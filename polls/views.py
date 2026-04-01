from typing import Dict, List
import csv
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.http import HttpResponse
from django.db import models
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, HRFlowable, Image
from reportlab.lib.units import inch, cm

from .forms import (
    DetectionRecordForm,
    LeafScanForm,
    YieldPredictionForm,
    YieldPredictionRecordForm,
    RegistrationForm,
    RiceVarietyForm,
    SeasonLogForm,
    FarmActivityForm,
    SiteSettingForm,
    KnowledgeEntryForm,
)
from .models import (
    DetectionRecord,
    YieldPrediction,
    Profile,
    RiceVariety,
    SeasonLog,
    FarmActivity,
    Field,
    PlantingRecord,
    HarvestRecord,
    SiteSetting,
    SiteSettingAudit,
    KnowledgeBaseEntry,
)
from . import services
from .decorators import admin_only, technician_or_admin, role_required, filter_queryset_by_role


RECENT_ACTIVITY_SESSION_KEY = "polls_recent_activity"


def _get_recent_activity(request) -> List[Dict[str, str]]:
    return request.session.get(RECENT_ACTIVITY_SESSION_KEY, [])


def _push_recent_activity(request, title: str) -> None:
    now = timezone.localtime()
    entry = {
        "title": title,
        "timestamp": now.strftime("%b %d, %Y %I:%M %p"),
    }
    history = _get_recent_activity(request)
    history.insert(0, entry)
    request.session[RECENT_ACTIVITY_SESSION_KEY] = history[:6]
    request.session.modified = True


def _build_query_string(request, remove_keys=('page',)):
    params = request.GET.copy()
    for key in remove_keys:
        params.pop(key, None)
    qs = params.urlencode()
    return f"&{qs}" if qs else ""


@login_required(login_url=reverse_lazy('polls:login'))
def dashboard(request):
    from django.db.models import Count
    from datetime import timedelta
    from decimal import Decimal
    
    # Get user profile
    user_profile = getattr(request.user, 'profile', None)
    role = user_profile.role if user_profile else 'farmer'
    
    # Role-based data filtering
    # Admin/Technician: See ALL data (system-wide stats)
    # Farmer: See only OWN data (personal stats)
    
    # Disease distribution for pie chart
    if user_profile:
        disease_qs = DetectionRecord.objects.filter(is_active=True)
        if role == 'farmer':
            disease_qs = disease_qs.filter(user=user_profile)
        # Exclude rejected/unclassified scans so chart only shows real diseases
        disease_stats = (
            disease_qs
            .exclude(disease__isnull=True)
            .exclude(disease__name__iexact='Unknown/Not Rice')
            .exclude(disease__name__iexact='Unknown')
            .values('disease__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )
    else:
        disease_stats = []
    
    # Detection trends (last 7 days)
    # BEST PRACTICE: Use timezone-aware date ranges instead of __date lookup
    # to avoid MySQL timezone conversion issues
    today = timezone.now().date()
    trend_data = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        # Create timezone-aware start and end of day
        start_of_day = timezone.make_aware(
            timezone.datetime.combine(date, timezone.datetime.min.time())
        )
        end_of_day = timezone.make_aware(
            timezone.datetime.combine(date, timezone.datetime.max.time())
        )
        
        if user_profile:
            trend_qs = DetectionRecord.objects.filter(
                is_active=True,
                created_at__gte=start_of_day,
                created_at__lte=end_of_day
            ).exclude(
                disease__name__iexact='Unknown/Not Rice'
            ).exclude(
                disease__name__iexact='Unknown'
            )
            if role == 'farmer':
                trend_qs = trend_qs.filter(user=user_profile)
            count = trend_qs.count()
        else:
            count = 0
        trend_data.append({'date': date.strftime('%m/%d'), 'count': count})
    
    # Get metrics
    metrics = services.dashboard_metrics(user_profile=user_profile, role=role)
    
    # Convert Decimal to float for JSON serialization
    def convert_decimals(data):
        if isinstance(data, list):
            return [convert_decimals(item) for item in data]
        elif isinstance(data, dict):
            return {key: convert_decimals(value) for key, value in data.items()}
        elif isinstance(data, Decimal):
            return float(data)
        return data
    
    metrics['avg_yield_by_barangay'] = convert_decimals(metrics['avg_yield_by_barangay'])
    metrics['avg_yield_by_field'] = convert_decimals(metrics['avg_yield_by_field'])
    
    context = {
        "recent_activity": _get_recent_activity(request),
        "disease_stats": list(disease_stats),
        "trend_data": trend_data,
        "is_admin": role == 'admin',
        "is_technician": role == 'technician',
        "role": role,
        **metrics,
    }

    return render(request, "core/dashboard.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect("polls:dashboard")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # BEST PRACTICE: Check account status before authentication
        try:
            user_check = User.objects.get(username=username)
            profile, _ = Profile.objects.get_or_create(user=user_check)
            
            # Check if account is deactivated
            if not user_check.is_active:
                messages.error(request, "Your account has been deactivated. Please contact the administrator for assistance.")
                return render(request, "auth/login.html")
            
            # Check if account is pending approval
            if not profile.is_approved:
                messages.warning(request, "Your account is pending approval. An administrator will review your registration soon.")
                return render(request, "auth/login.html")
        except User.DoesNotExist:
            # User doesn't exist, will be caught by authenticate below
            pass
        
        # Now authenticate with password
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("polls:dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "auth/login.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("polls:dashboard")
    
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        
        # BEST PRACTICE: get_or_create to avoid duplicate errors
        # Signal already creates profile, but this ensures role is "farmer"
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={'role': 'farmer', 'is_approved': False}
        )
        
        # If profile already exists (from signal), update it
        if not created:
            profile.role = 'farmer'
            profile.is_approved = False
            profile.save()
        
        messages.success(
            request, 
            f"Welcome to AgriScan+, {user.username}! Your account is pending admin approval."
        )

        # Email all admin accounts: "New farmer pending approval"
        try:
            from django.contrib.auth.models import User as _User
            from . import services as _svc
            # Tagalog: para walang hardcoded localhost, gamitin ang base URL mula .env.
            admin_users_url = _svc._app_url('/admin-users/')
            admin_emails = list(
                _User.objects.filter(profile__role='admin', is_active=True)
                .exclude(email='')
                .values_list('email', flat=True)
            )
            for admin_email in admin_emails:
                _svc.send_plain_email(
                    recipient_email=admin_email,
                    subject='[AgriScan+] New Farmer Registration Pending Approval',
                    body=(
                        f"Hello Admin,\n\n"
                        f"A new farmer account has been registered and is waiting for your approval.\n\n"
                        f"Username : {user.username}\n"
                        f"Full name: {user.get_full_name() or '(not set)'}\n"
                        f"Email    : {user.email or '(not set)'}\n\n"
                        f"Review and approve the account here:\n"
                        f"{admin_users_url}\n\n"
                        f"---\nAgriScan+ System"
                    ),
                )
        except Exception:
            pass  # Never block registration on email failure

        return redirect("polls:login")  # Redirect to login, not dashboard
    
    return render(request, "auth/register.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("polls:login")


@login_required(login_url=reverse_lazy('polls:login'))
def profile(request):
    # Get or create Profile for the logged-in user
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    form = None
    from .forms import ProfileForm
    if request.method == "POST":
        form = ProfileForm(request.POST, user=request.user, profile=profile_obj)
        if form.is_valid():
            form.save(request.user, profile_obj)
            messages.success(request, "Profile updated.")
            return redirect("polls:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(user=request.user, profile=profile_obj)

    # BEST PRACTICE: Role-based activity stats
    # Farmers: Show only their own records
    # Admin/Technician: Show system-wide stats
    role = profile_obj.role if profile_obj else 'farmer'
    
    if role == 'farmer':
        # Farmer sees only their own activity
        scans = DetectionRecord.objects.filter(user=profile_obj, is_active=True).count()
        yield_predictions = YieldPrediction.objects.filter(
            planting__field__owner=profile_obj, is_active=True
        ).count()
    else:
        # Admin/Technician sees system-wide stats
        scans = DetectionRecord.objects.filter(is_active=True).count()
        yield_predictions = YieldPrediction.objects.filter(is_active=True).count()
    
    stats = {
        "scans": scans,
        "yield_predictions": yield_predictions,
        "reports": scans + yield_predictions,  # Total activity
    }

    return render(request, "account/profile.html", {"form": form, "profile": profile_obj, "stats": stats})


@login_required(login_url=reverse_lazy('polls:login'))
def change_password(request):
    """
    Change password view for all user roles.
    BEST PRACTICES:
    - Requires authentication (@login_required)
    - Validates old password before allowing change
    - Uses Django's built-in password validators
    - Updates session to prevent logout after password change
    - Provides clear feedback messages
    - Logs password changes for security audit
    """
    from .forms import CustomPasswordChangeForm
    from django.contrib.auth import update_session_auth_hash
    
    if request.method == "POST":
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Important: Update session hash so user doesn't get logged out
            update_session_auth_hash(request, user)
            
            # Log activity
            _push_recent_activity(request, "Password changed successfully")
            
            messages.success(
                request, 
                "Your password has been changed successfully! Your account is now more secure."
            )
            return redirect("polls:profile")
        else:
            messages.error(
                request, 
                "Please correct the errors below. Make sure your old password is correct."
            )
    else:
        form = CustomPasswordChangeForm(user=request.user)
    
    # Get user role for template context
    user_profile = getattr(request.user, 'profile', None)
    role = user_profile.role if user_profile else 'farmer'
    
    context = {
        'form': form,
        'profile': user_profile,
        'role': role,
    }
    return render(request, "account/change_password.html", context)


@login_required(login_url=reverse_lazy('polls:login'))
def scan(request):
    result = None
    result_image_url = None
    error = None
    detection_record = None
    detailed_treatment = None  # For comprehensive treatment info
    
    # Get user profile for field/planting filtering
    user_profile = getattr(request.user, 'profile', None)
    form = LeafScanForm(request.POST or None, request.FILES or None, user=request.user)

    if request.method == "POST" and form.is_valid():
        try:
            saved_path, rel_path = services.save_detection_image(form.cleaned_data["leaf_image"])
            prediction = services.classify_leaf_image(saved_path)
            result = prediction.to_template_dict()
            result_image_url = f"{settings.MEDIA_URL}{rel_path}"
            
            # Get detailed treatment information
            detailed_treatment = services.get_detailed_treatment(
                prediction.label, 
                prediction.severity_pct
            )
            
            # Get planting from form (field is derived from planting.field)
            planting = form.cleaned_data.get("planting")
            
            # Store detection with planting and user info
            detection_record = services.store_detection_result(
                prediction, 
                rel_path,
                planting=planting,
                user=user_profile
            )
            if detection_record:
                messages.success(request, "Detection saved.")
            _push_recent_activity(
                request,
                f"Leaf scan: {result['disease']} ({result['confidence']}% confidence)",
            )
        except Exception as exc:  # pylint: disable=broad-except
            error = str(exc)
    elif request.method == "POST":
        error = "Please upload a valid image before submitting."

    context = {
        "form": form,
        "result": result,
        "result_image_url": result_image_url,
        "error": error,
        "detection_record": detection_record,
        "detailed_treatment": detailed_treatment,  # Pass detailed treatment to template
    }
    return render(request, "tools/scan.html", context)


@login_required(login_url=reverse_lazy('polls:login'))
def camera_capture(request):
    """Camera capture page for taking photos with device camera."""
    return render(request, "tools/best_camera.html")


@login_required(login_url=reverse_lazy('polls:login'))
def yield_prediction(request):
    variety_choices = services.get_variety_choices()
    yield_result = None
    error = None
    yield_record = None
    detection = None
    planting = None  # Selected planting record
    
    # BEST PRACTICE: Check if detection_id is provided (from scan results)
    detection_id = request.GET.get('detection_id')
    initial_data = {}
    from_detection = False  # Flag to hide planting selector
    
    if detection_id:
        from_detection = True  # Coming from scan - hide planting selector
        try:
            detection = DetectionRecord.objects.select_related(
                'planting', 'planting__field', 'planting__variety'
            ).get(pk=detection_id)
            
            # Pre-fill form with detection data (BEST PRACTICE)
            if detection.planting:
                planting = detection.planting
                if planting.variety:
                    initial_data['variety'] = planting.variety.code
                if planting.field:
                    initial_data['area'] = float(planting.field.area_hectares)
                if planting.planting_date:
                    initial_data['planting_date'] = planting.planting_date
                    
                    # Calculate growth duration from expected harvest date
                    if planting.expected_harvest_date:
                        days = (planting.expected_harvest_date - planting.planting_date).days
                    else:
                        # Fallback: use variety's average growth days or default 120
                        days = planting.variety.average_growth_days if planting.variety else 120
                    initial_data['average_growth_duration_days'] = days
                
                # Pre-fill historical data using actual harvest records if available.
                # This keeps the prediction tool using real measured yield instead of
                # legacy manual values stored on the PlantingRecord.
                hist = services.get_historical_yield_data(planting)
                initial_data['historical_production_tons'] = float(hist.get('historical_production') or 0.0)
                initial_data['historical_yield_tons_per_ha'] = float(hist.get('historical_yield') or 0.0)
            
            # Set health from detection
            initial_data['health'] = str(detection_id)

            # Tagalog: Ipakita ang season at ecosystem type (read-only display lang)
            # mula sa planting record at its associated field.
            if planting:
                initial_data['season'] = planting.get_season_display() if planting.season else planting.season
                # Ecosystem type can be blank; show raw value if no display label.
                if planting.field:
                    initial_data['ecosystem_type'] = (
                        planting.field.get_ecosystem_type_display() 
                        if planting.field.ecosystem_type 
                        else planting.field.ecosystem_type
                    )
        except DetectionRecord.DoesNotExist:
            messages.warning(request, f"Detection #{detection_id} not found.")

    if request.method == "POST":
        # Pass initial_data so display-only fields (season/ecosystem) persist even when the
        # form is re-rendered after validation errors (they are disabled and not posted).
        form = YieldPredictionForm(
            request.POST,
            initial=initial_data,
            variety_choices=variety_choices,
            user=request.user,
        )
        if form.is_valid():
            try:
                # BEST PRACTICE: Check if planting record was selected
                planting = form.cleaned_data.get("planting")

                # use_manual_data=1 means user edited some fields manually while a
                # planting was selected.  We still KEEP the planting FK for ownership
                # tracking, but use the form values for the prediction itself.
                use_manual_data = request.POST.get("use_manual_data", "0") == "1"

                # When arriving from a detection scan, enforce that the planted
                # cycle is the one from the detection (locked fields). This prevents
                # users from tampering with core planting inputs.
                lock_core_fields = from_detection and detection and detection.planting
                if lock_core_fields:
                    planting = detection.planting

                # Use planting data when either the user did not manually override,
                # or when core fields are locked due to coming from a detection scan.
                if planting and (not use_manual_data or lock_core_fields):
                    # ── Pure planting-record path ──────────────────────────────
                    # Core prediction inputs come from the linked PlantingRecord.
                    hist = services.get_historical_yield_data(planting)
                    prediction_data = {
                        "variety": planting.variety.code,
                        "field_area_ha": float(planting.field.area_hectares),
                        "historical_production_tons": float(hist.get('historical_production') or 0.0),
                        "historical_yield_tons_per_ha": float(hist.get('historical_yield') or 0.0),
                        "planting_date": planting.planting_date,
                        "average_growth_duration_days": planting.average_growth_duration_days or 120,
                    }

                    # Allow users to override only the historical production/yield
                    # when core fields are locked (detection flow).
                    if lock_core_fields and use_manual_data:
                        if form.cleaned_data.get('historical_production_tons') is not None:
                            prediction_data['historical_production_tons'] = float(form.cleaned_data['historical_production_tons'])
                        if form.cleaned_data.get('historical_yield_tons_per_ha') is not None:
                            prediction_data['historical_yield_tons_per_ha'] = float(form.cleaned_data['historical_yield_tons_per_ha'])

                    # FIXED: Use health status from FORM (user's selection), not auto-detected
                    health_value = form.cleaned_data.get("health")
                    if health_value:
                        try:
                            det_id = int(health_value)
                            detection = DetectionRecord.objects.select_related(
                                'planting', 'planting__field', 'planting__variety', 'disease'
                            ).get(pk=det_id)
                            # Convert severity to health value (0=healthy, 1=diseased)
                            health_numeric = detection.severity_pct / 100.0 if detection.severity_pct else 0.5
                            health_display = f"{detection.disease.name} ({detection.severity_pct}%)" if detection.disease else "Detected"
                            prediction_data["health_status"] = health_numeric
                        except (ValueError, DetectionRecord.DoesNotExist):
                            # Fallback to numeric value
                            health_numeric = float(health_value) if health_value else 0.0
                            health_display = {"0": "Healthy", "0.5": "Moderate", "1.0": "Diseased"}.get(str(health_value), "Unknown")
                            prediction_data["health_status"] = health_numeric
                    else:
                        # No health selection - default to healthy
                        prediction_data["health_status"] = 0.0
                        health_display = "Healthy (no detection selected)"
                        detection = None

                    variety_display = planting.variety.code
                    area = float(planting.field.area_hectares)

                else:
                    # ── Manual entry path (or manual-override with planting linked) ──
                    # Use form values for the prediction.
                    # `planting` is kept as-is for ownership/FK — not cleared.
                    prediction_data = {
                        "variety": form.cleaned_data["variety"],
                        "field_area_ha": float(form.cleaned_data["area"]),
                        "historical_production_tons": float(form.cleaned_data["historical_production_tons"]),
                        "historical_yield_tons_per_ha": float(form.cleaned_data["historical_yield_tons_per_ha"]),
                        "planting_date": form.cleaned_data["planting_date"],
                        "average_growth_duration_days": int(form.cleaned_data["average_growth_duration_days"]),
                    }
                    # Handle health status from form (detection ID or numeric value)
                    health_value = form.cleaned_data.get("health")
                    if health_value:
                        try:
                            det_id = int(health_value)
                            detection = DetectionRecord.objects.select_related(
                                'planting', 'planting__field', 'planting__variety'
                            ).get(pk=det_id)
                            # Convert severity to health value (0=healthy, 1=diseased)
                            health_numeric = detection.severity_pct / 100.0 if detection.severity_pct else 0.5
                            health_display = f"{detection.disease.name} ({detection.severity_pct}%)"
                            prediction_data["health_status"] = health_numeric
                            
                            # If detection has planting, link it
                            if detection.planting:
                                planting = detection.planting
                        except (ValueError, DetectionRecord.DoesNotExist):
                            # Fallback to numeric value
                            health_numeric = float(health_value) if health_value else 0.0
                            health_display = {"0": "Healthy", "0.5": "Moderate", "1.0": "Diseased"}.get(str(health_value), "Unknown")
                            prediction_data["health_status"] = health_numeric
                    else:
                        prediction_data["health_status"] = 0.0
                        health_display = "Healthy"
                    
                    variety_display = form.cleaned_data["variety"]
                    area = float(form.cleaned_data["area"])

                    # Only inherit area from detection.planting when this is a
                    # pure manual-entry session (no planting was selected at all).
                    # When use_manual_data=1, the user intentionally typed their own
                    # area value — respect it.
                    if not use_manual_data and detection and detection.planting and detection.planting.field:
                        area = float(detection.planting.field.area_hectares)
                
                # BEST PRACTICE: Pass detection to predict_yield
                # When use_manual_data=1 the user's typed values are already in
                # prediction_data — tell predict_yield NOT to override them with
                # detection.planting data (still uses detection for health_status).
                prediction = services.predict_yield(
                    prediction_data,
                    detection=detection,
                    override_with_detection=(not use_manual_data),
                )
                yield_result = prediction.to_template_dict()
                yield_result.update(
                    {
                        "area": round(area, 2),
                        "variety": variety_display,
                        "health": health_display,
                    }
                )
                yield_record = services.store_yield_prediction(
                    prediction, form.cleaned_data, detection, planting=planting
                )
                if yield_record:
                    messages.success(request, f"Yield prediction saved: {yield_result['value_display']} ({yield_result['readiness_display']})")
                _push_recent_activity(
                    request,
                    f"Yield prediction: {yield_result['value']} tons/ha ({yield_result['yield_readiness']}) across {area:.2f} ha",
                )
            except Exception as exc:  # pylint: disable=broad-except
                error = str(exc)
        else:
            error = "Please correct the fields highlighted below."
    else:
        form = YieldPredictionForm(initial=initial_data, variety_choices=variety_choices, user=request.user)

    context = {
        "form": form,
        "yield_result": yield_result,
        "error": error,
        "yield_record": yield_record,
        "from_detection": from_detection,  # Hide planting selector if from scan
        "detection": detection,  # Pass detection object for auto-fill info
    }
    return render(request, "tools/yield_prediction.html", context)


@login_required(login_url=reverse_lazy('polls:login'))
def reports(request):
    """
    Reports & Analytics with BEST PRACTICE features:
    - Custom date range filtering
    - Export to PDF/CSV
    - Role-based data access
    - Performance metrics
    """
    from django.db.models import Count, Avg, Q
    from datetime import timedelta, datetime
    import calendar
    
    # Get user profile
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    # Get role for filtering
    role = user_profile.role
    
    # BEST PRACTICE: Custom date range filtering
    today = timezone.now().date()
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    # Default: last 6 months
    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            start_date = today - timedelta(days=180)
            end_date = today
    else:
        start_date = today - timedelta(days=180)
        end_date = today
    
    # BEST PRACTICE: Export functionality
    export_format = request.GET.get('export')
    if export_format in ['pdf', 'csv']:
        # Parse which sections the user selected (default: all)
        all_sections = ['summary', 'monthly', 'diseases', 'varieties', 'detections', 'yields']
        requested = request.GET.getlist('sections')
        sections = set(requested) if requested else set(all_sections)
        return _export_report(request, export_format, start_date, end_date, role, user_profile, sections)
    
    # Monthly detection stats (dynamic based on date range) - filtered by role
    monthly_data = []
    current_date = start_date.replace(day=1)
    end_month = end_date.replace(day=1)
    
    while current_date <= end_month:
        month_start = current_date
        month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        # BEST PRACTICE: Use timezone-aware date ranges instead of __date lookup
        month_start_dt = timezone.make_aware(
            timezone.datetime.combine(month_start, timezone.datetime.min.time())
        )
        month_end_dt = timezone.make_aware(
            timezone.datetime.combine(month_end, timezone.datetime.max.time())
        )
        
        detection_qs = DetectionRecord.objects.filter(
            is_active=True,
            created_at__gte=month_start_dt,
            created_at__lte=month_end_dt
        )
        # Apply role filtering
        if role == 'farmer':
            detection_qs = detection_qs.filter(user=user_profile)
        
        healthy = detection_qs.filter(disease__name__iexact='healthy').count()
        diseased = detection_qs.exclude(disease__name__iexact='healthy').count()
        
        monthly_data.append({
            'month': month_start.strftime('%b %Y'),
            'healthy': healthy,
            'diseased': diseased,
            'total': healthy + diseased
        })
        
        # Move to next month
        current_date = (month_start + timedelta(days=32)).replace(day=1)
    
    # BEST PRACTICE: Create timezone-aware date range for filtering
    start_date_dt = timezone.make_aware(
        timezone.datetime.combine(start_date, timezone.datetime.min.time())
    )
    end_date_dt = timezone.make_aware(
        timezone.datetime.combine(end_date, timezone.datetime.max.time())
    )
    
    # Average yield per variety - group by actual variety FK, not model_meta string
    yield_qs = YieldPrediction.objects.filter(
        is_active=True,
        created_at__gte=start_date_dt,
        created_at__lte=end_date_dt
    )
    if role == 'farmer':
        yield_qs = yield_qs.filter(planting__field__owner=user_profile)

    variety_stats = (
        yield_qs
        .filter(planting__variety__isnull=False)   # exclude unlinked / no-variety records
        .values('planting__variety__code', 'planting__variety__name')
        .annotate(
            avg_sacks=Avg('predicted_sacks_per_ha'),
            avg_tons=Avg('predicted_yield_tons_per_ha'),
            count=Count('id'),
        )
        .order_by('-avg_sacks')[:10]
    )
    variety_yields = []
    for stat in variety_stats:
        code = stat['planting__variety__code'] or stat['planting__variety__name'] or 'Unknown'
        variety_yields.append({
            'variety': code,
            'avg_sacks': round(float(stat['avg_sacks'] or 0), 2),
            'avg_tons': round(float(stat['avg_tons'] or 0), 2),
            'count': stat['count'],
        })

    # Count unlinked predictions separately so they stay visible in the summary
    unlinked_count = yield_qs.filter(planting__variety__isnull=True).count()

    # Model accuracy metrics - filtered by role and date range
    active_model = services._get_active_model_version()
    model_accuracy = float(active_model.accuracy) if active_model and active_model.accuracy else None

    detection_total_qs = DetectionRecord.objects.filter(
        is_active=True,
        created_at__gte=start_date_dt,
        created_at__lte=end_date_dt
    )
    if role == 'farmer':
        detection_total_qs = detection_total_qs.filter(user=user_profile)

    total_detections = detection_total_qs.count()
    healthy_count    = detection_total_qs.filter(disease__name__iexact='healthy').count()
    diseased_count   = total_detections - healthy_count
    high_confidence  = detection_total_qs.filter(confidence_pct__gte=80).count()
    confidence_rate  = round((high_confidence / total_detections * 100) if total_detections > 0 else 0, 1)

    # Disease frequency ranking (top 10 — exclude healthy, unknown/not-rice, and null disease)
    _EXCLUDE_FROM_DISEASE_FREQ = ['healthy', 'unknown/not rice', 'unknown']
    disease_freq = list(
        detection_total_qs
        .exclude(disease__isnull=True)
        .exclude(disease__name__iexact='healthy')
        .exclude(disease__name__iexact='Unknown/Not Rice')
        .exclude(disease__name__iexact='Unknown')
        .values('disease__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )
    # Count the excluded "junk" detections separately for transparency
    unclassified_count = detection_total_qs.filter(
        models.Q(disease__isnull=True) |
        models.Q(disease__name__iexact='Unknown/Not Rice') |
        models.Q(disease__name__iexact='Unknown')
    ).count()
    # Compute pct share of each disease relative to diseased total
    for row in disease_freq:
        row['pct'] = round((row['count'] / diseased_count * 100) if diseased_count else 0, 1)

    # Extra summary counts
    from polls.models import PlantingRecord, Field
    planting_qs = PlantingRecord.objects.filter(
        is_active=True,
        planting_date__gte=start_date,
        planting_date__lte=end_date,
    )
    field_qs = Field.objects.filter(is_active=True)
    if role == 'farmer':
        planting_qs = planting_qs.filter(field__owner=user_profile)
        field_qs    = field_qs.filter(owner=user_profile)
    total_plantings = planting_qs.count()
    total_fields    = field_qs.count()

    context = {
        'monthly_data': monthly_data,
        'variety_yields': variety_yields,
        'unlinked_yield_count': unlinked_count,
        'disease_freq': disease_freq,
        'unclassified_count': unclassified_count,
        'model_accuracy': model_accuracy,
        'confidence_rate': confidence_rate,
        'total_detections': total_detections,
        'total_yields': yield_qs.count(),
        'healthy_count': healthy_count,
        'diseased_count': diseased_count,
        'total_plantings': total_plantings,
        'total_fields': total_fields,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'role': role,
    }
    return render(request, 'account/reports.html', context)


def _export_report(request, format_type, start_date, end_date, role, user_profile, sections=None):
    """
    BEST PRACTICE: Export reports to PDF or CSV format.
    Supports role-based data filtering with timezone-aware queries.
    `sections` is a set of section keys to include:
      summary | monthly | diseases | varieties | detections | yields
    If None, all sections are included.
    """
    from django.db.models import Count, Avg
    import csv

    ALL_SECTIONS = {'summary', 'monthly', 'diseases', 'varieties', 'detections', 'yields'}
    if not sections:
        sections = ALL_SECTIONS

    # Timezone-aware date range
    start_date_dt = timezone.make_aware(
        timezone.datetime.combine(start_date, timezone.datetime.min.time())
    )
    end_date_dt = timezone.make_aware(
        timezone.datetime.combine(end_date, timezone.datetime.max.time())
    )

    # Base querysets — role filtered, active only
    detection_qs = DetectionRecord.objects.filter(
        is_active=True,
        created_at__gte=start_date_dt,
        created_at__lte=end_date_dt
    ).select_related('disease', 'planting__field')
    if role == 'farmer':
        detection_qs = detection_qs.filter(user=user_profile)

    yield_qs = YieldPrediction.objects.filter(
        is_active=True,
        created_at__gte=start_date_dt,
        created_at__lte=end_date_dt
    ).select_related('planting__variety', 'planting__field')
    if role == 'farmer':
        yield_qs = yield_qs.filter(planting__field__owner=user_profile)

    # ── Pre-compute shared stats ──────────────────────────────────────────
    total_detections   = detection_qs.count()
    healthy_count      = detection_qs.filter(disease__name__iexact='healthy').count()
    diseased_count     = total_detections - healthy_count
    high_conf_count    = detection_qs.filter(confidence_pct__gte=80).count()
    confidence_rate    = round((high_conf_count / total_detections * 100) if total_detections else 0, 1)

    total_yields       = yield_qs.count()
    avg_yield_val      = yield_qs.aggregate(v=Avg('predicted_sacks_per_ha'))['v']
    avg_yield          = round(float(avg_yield_val or 0), 2)

    # Monthly breakdown
    from datetime import timedelta
    monthly_rows = []
    cur = start_date.replace(day=1)
    end_month = end_date.replace(day=1)
    while cur <= end_month:
        m_start = timezone.make_aware(timezone.datetime.combine(cur, timezone.datetime.min.time()))
        next_month = (cur + timedelta(days=32)).replace(day=1)
        m_end = timezone.make_aware(timezone.datetime.combine(
            next_month - timedelta(days=1), timezone.datetime.max.time()
        ))
        mq = detection_qs.filter(created_at__gte=m_start, created_at__lte=m_end)
        h = mq.filter(disease__name__iexact='healthy').count()
        d = mq.count() - h
        monthly_rows.append({'month': cur.strftime('%b %Y'), 'healthy': h, 'diseased': d, 'total': h + d})
        cur = next_month

    # Disease frequency ranking — exclude healthy, unknown/not-rice, null disease
    disease_freq = (
        detection_qs
        .exclude(disease__isnull=True)
        .exclude(disease__name__iexact='healthy')
        .exclude(disease__name__iexact='Unknown/Not Rice')
        .exclude(disease__name__iexact='Unknown')
        .values('disease__name')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )
    unclassified_export_count = detection_qs.filter(
        models.Q(disease__isnull=True) |
        models.Q(disease__name__iexact='Unknown/Not Rice') |
        models.Q(disease__name__iexact='Unknown')
    ).count()

    # Variety yield breakdown — exclude unlinked records (no variety FK)
    variety_stats = (
        yield_qs
        .filter(planting__variety__isnull=False)
        .values('planting__variety__code', 'planting__variety__name')
        .annotate(avg_sacks=Avg('predicted_sacks_per_ha'), avg_tons=Avg('predicted_yield_tons_per_ha'), count=Count('id'))
        .order_by('-avg_sacks')
    )
    variety_rows = []
    for stat in variety_stats:
        code = stat['planting__variety__code'] or stat['planting__variety__name'] or '—'
        variety_rows.append({
            'variety': code,
            'avg_sacks': round(float(stat['avg_sacks'] or 0), 2),
            'avg_tons': round(float(stat['avg_tons'] or 0), 2),
            'count': stat['count'],
        })
    unlinked_export_count = yield_qs.filter(planting__variety__isnull=True).count()

    # ── Model accuracy ────────────────────────────────────────────────────
    active_model   = services._get_active_model_version()
    model_accuracy = float(active_model.accuracy) if active_model and active_model.accuracy else None

    generated_at = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    generated_by = request.user.get_full_name() or request.user.username

    # ═══════════════════════════════════════════════════════════════════════
    # CSV EXPORT
    # ═══════════════════════════════════════════════════════════════════════
    if format_type == 'csv':
        response = HttpResponse(
            content_type='text/csv; charset=utf-8-sig'  # UTF-8 BOM — Excel opens correctly
        )
        fname = f'agriscan_report_{start_date}_{end_date}.csv'
        response['Content-Disposition'] = f'attachment; filename="{fname}"'

        w = csv.writer(response)

        # ── Cover ──
        w.writerow(['AgriScan+ Analytics Report'])
        w.writerow(['Date Range', f'{start_date} to {end_date}'])
        w.writerow(['Generated', generated_at])
        w.writerow(['Generated By', generated_by])
        w.writerow([])

        # ── Section 1: Detection Summary ──
        if 'summary' in sections:
            w.writerow(['=== DETECTION SUMMARY ==='])
            w.writerow(['Metric', 'Value'])
            w.writerow(['Total Detections', total_detections])
            w.writerow(['Healthy Crops', healthy_count])
            w.writerow(['Diseased Crops', diseased_count])
            w.writerow([f'High Confidence (>=80%)', high_conf_count])
            w.writerow(['Confidence Rate (%)', confidence_rate])
            w.writerow(['CNN Model Accuracy (%)', model_accuracy])
            w.writerow([])

        # ── Section 2: Yield Summary ──
        if 'summary' in sections:
            w.writerow(['=== YIELD PREDICTION SUMMARY ==='])
            w.writerow(['Metric', 'Value'])
            w.writerow(['Total Predictions', total_yields])
            w.writerow(['Average Predicted Yield (sacks/ha)', avg_yield])
            w.writerow([])

        # ── Section 3: Monthly Breakdown ──
        if 'monthly' in sections:
            w.writerow(['=== MONTHLY DETECTION BREAKDOWN ==='])
            w.writerow(['Month', 'Healthy', 'Diseased', 'Total'])
            for row in monthly_rows:
                w.writerow([row['month'], row['healthy'], row['diseased'], row['total']])
            w.writerow([])

        # ── Section 4: Disease Frequency ──
        if 'diseases' in sections:
            w.writerow(['=== TOP DISEASE FREQUENCY (real diseases only) ==='])
            if unclassified_export_count:
                w.writerow([f'Note: {unclassified_export_count} unclassified/rejected scan(s) excluded (Unknown / Unknown/Not Rice)'])
            w.writerow(['Disease', 'Detection Count'])
            for row in disease_freq:
                w.writerow([row['disease__name'], row['count']])
            w.writerow([])

        # ── Section 5: Variety Yield ──
        if 'varieties' in sections:
            w.writerow(['=== AVERAGE YIELD PER VARIETY (linked records only) ==='])
            if unlinked_export_count:
                w.writerow([f'Note: {unlinked_export_count} prediction(s) excluded — no variety linked'])
            w.writerow(['Variety', 'Avg Sacks/ha', 'Avg Tons/ha', 'Prediction Count'])
            for row in variety_rows:
                w.writerow([row['variety'], row['avg_sacks'], row['avg_tons'], row['count']])
            w.writerow([])

        # ── Section 6: Detection Details (all rows, no arbitrary cap) ──
        if 'detections' in sections:
            det_total = detection_qs.count()
            w.writerow([f'=== DETECTION DETAILS ({det_total} records) ==='])
            w.writerow(['Date', 'Disease', 'Confidence (%)', 'Severity (%)', 'Field', 'Source'])
            for det in detection_qs.order_by('-created_at'):
                field_name = det.planting.field.name if det.planting and det.planting.field else 'N/A'
                w.writerow([
                    det.created_at.strftime('%Y-%m-%d %H:%M'),
                    det.disease.name if det.disease else 'Healthy',
                    round(float(det.confidence_pct or 0), 2),
                    round(float(det.severity_pct or 0), 1) if det.severity_pct else '',
                    field_name,
                    det.source or '',
                ])
            w.writerow([])

        # ── Section 7: Yield Details (all rows) ──
        if 'yields' in sections:
            yld_total = yield_qs.count()
            w.writerow([f'=== YIELD PREDICTION DETAILS ({yld_total} records) ==='])
            w.writerow(['Date', 'Variety', 'Field', 'Sacks/ha', 'Total Sacks', 'Total Tons', 'Harvest Date'])
            for rec in yield_qs.order_by('-created_at'):
                variety = rec.planting.variety.code if rec.planting and rec.planting.variety else 'N/A'
                field   = rec.planting.field.name   if rec.planting and rec.planting.field   else 'N/A'
                w.writerow([
                    rec.created_at.strftime('%Y-%m-%d %H:%M'),
                    variety,
                    field,
                    rec.predicted_sacks_per_ha or '',
                    rec.total_sacks or '',
                    rec.total_tons or '',
                    rec.harvest_date.strftime('%Y-%m-%d') if rec.harvest_date else '',
                ])

        return response

    # ═══════════════════════════════════════════════════════════════════════
    # PDF EXPORT
    # ═══════════════════════════════════════════════════════════════════════
    elif format_type == 'pdf':
        GREEN  = colors.HexColor('#16a34a')
        BLUE   = colors.HexColor('#1e40af')
        LGRAY  = colors.HexColor('#f3f4f6')
        DGRAY  = colors.HexColor('#374151')
        WHITE  = colors.white
        RED    = colors.HexColor('#dc2626')
        YELLOW = colors.HexColor('#d97706')

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=1.5*cm, leftMargin=1.5*cm,
            topMargin=1.5*cm, bottomMargin=1.5*cm,
        )

        styles = getSampleStyleSheet()
        H1 = ParagraphStyle('H1', parent=styles['Heading1'],
            fontSize=22, textColor=GREEN, spaceAfter=4, alignment=1)
        H2 = ParagraphStyle('H2', parent=styles['Heading2'],
            fontSize=13, textColor=BLUE, spaceBefore=14, spaceAfter=6)
        SMALL = ParagraphStyle('SMALL', parent=styles['Normal'],
            fontSize=8, textColor=DGRAY)
        META = ParagraphStyle('META', parent=styles['Normal'],
            fontSize=9, textColor=DGRAY, spaceAfter=2)

        def header_style(bg=BLUE):
            return TableStyle([
                ('BACKGROUND',    (0, 0), (-1, 0), bg),
                ('TEXTCOLOR',     (0, 0), (-1, 0), WHITE),
                ('FONTNAME',      (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE',      (0, 0), (-1, 0), 9),
                ('ALIGN',         (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE',      (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS',(0, 1), (-1, -1), [WHITE, LGRAY]),
                ('GRID',          (0, 0), (-1, -1), 0.4, colors.HexColor('#d1d5db')),
                ('TOPPADDING',    (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING',   (0, 0), (-1, -1), 6),
            ])

        elems = []

        # ── Cover ──
        elems.append(Paragraph('AgriScan+ Analytics Report', H1))
        elems.append(HRFlowable(width='100%', thickness=1, color=GREEN, spaceAfter=8))
        elems.append(Paragraph(f'<b>Date Range:</b> {start_date} to {end_date}', META))
        elems.append(Paragraph(f'<b>Generated:</b> {generated_at}', META))
        elems.append(Paragraph(f'<b>Prepared by:</b> {generated_by}', META))
        elems.append(Spacer(1, 10))

        # ── Section 1: KPI Summary ──
        if 'summary' in sections:
            elems.append(Paragraph('1. Summary Statistics', H2))
            kpi_data = [
                ['Metric', 'Value'],
                ['Total Detections',              str(total_detections)],
                ['  Healthy Crops',               str(healthy_count)],
                ['  Diseased Crops',              str(diseased_count)],
                [f'  High Confidence (>=80%)',    str(high_conf_count)],
                ['Confidence Rate',               f'{confidence_rate}%'],
                ['CNN Model Accuracy',            f'{model_accuracy}%'],
                ['Total Yield Predictions',       str(total_yields)],
                ['Average Predicted Yield (sacks/ha)', str(avg_yield)],
            ]
            kpi_table = Table(kpi_data, colWidths=[4.5*inch, 2*inch])
            kpi_table.setStyle(header_style(BLUE))
            elems.append(kpi_table)
            elems.append(Spacer(1, 10))

        # ── Section 2: Monthly Breakdown ──
        if 'monthly' in sections:
            elems.append(Paragraph('2. Monthly Detection Breakdown', H2))
            month_data = [['Month', 'Healthy', 'Diseased', 'Total']]
            for row in monthly_rows:
                month_data.append([row['month'], str(row['healthy']), str(row['diseased']), str(row['total'])])
            month_table = Table(month_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            month_table.setStyle(header_style(GREEN))
            elems.append(month_table)
            elems.append(Spacer(1, 10))

        # ── Section 3: Disease Frequency ──
        if 'diseases' in sections:
            suffix = f' ({unclassified_export_count} unclassified excluded)' if unclassified_export_count else ''
            elems.append(Paragraph(f'3. Top Disease Frequency{suffix}', H2))
            dis_data = [['Disease', 'Detection Count']]
            for row in disease_freq:
                dis_data.append([row['disease__name'], str(row['count'])])
            if len(dis_data) == 1:
                dis_data.append(['No disease detections in range', ''])
            dis_table = Table(dis_data, colWidths=[4*inch, 2*inch])
            dis_table.setStyle(header_style(RED))
            elems.append(dis_table)
            elems.append(Spacer(1, 10))

        # ── Section 4: Variety Yield ──
        if 'varieties' in sections:
            suffix = f' ({unlinked_export_count} unlinked excluded)' if unlinked_export_count else ''
            elems.append(Paragraph(f'4. Average Yield per Rice Variety{suffix}', H2))
            var_data = [['Variety', 'Avg Sacks/ha', 'Avg Tons/ha', 'Predictions']]
            for row in variety_rows:
                var_data.append([row['variety'], str(row['avg_sacks']), str(row['avg_tons']), str(row['count'])])
            if len(var_data) == 1:
                var_data.append(['No yield data in range', '', '', ''])
            var_table = Table(var_data, colWidths=[3*inch, 1.7*inch, 1.7*inch, 1.5*inch])
            var_table.setStyle(header_style(YELLOW))
            elems.append(var_table)

        # ── Page Break → Detail Tables (only if detail sections selected) ──
        if 'detections' in sections or 'yields' in sections:
            elems.append(PageBreak())

        # ── Section 5: Detection Details ──
        if 'detections' in sections:
            det_total = detection_qs.count()
            elems.append(Paragraph(f'5. Detection Details ({det_total} records)', H2))
            det_data = [['Date', 'Disease', 'Confidence', 'Severity', 'Field']]
            for det in detection_qs.order_by('-created_at'):
                field_name = det.planting.field.name if det.planting and det.planting.field else 'N/A'
                det_data.append([
                    det.created_at.strftime('%Y-%m-%d'),
                    (det.disease.name if det.disease else 'Healthy')[:22],
                    f"{round(float(det.confidence_pct or 0), 1)}%",
                    f"{round(float(det.severity_pct or 0), 1)}%" if det.severity_pct else '-',
                    field_name[:24],
                ])
            det_table = Table(det_data, colWidths=[1.4*inch, 2.2*inch, 1.2*inch, 1.2*inch, 2.2*inch])
            det_table.setStyle(header_style(GREEN))
            elems.append(det_table)
            elems.append(Spacer(1, 10))

        # ── Section 6: Yield Details ──
        if 'yields' in sections:
            yld_total = yield_qs.count()
            elems.append(Paragraph(f'6. Yield Prediction Details ({yld_total} records)', H2))
            yld_data = [['Date', 'Variety', 'Field', 'Sacks/ha', 'Total Sacks', 'Harvest Date']]
            for rec in yield_qs.order_by('-created_at'):
                variety = rec.planting.variety.code if rec.planting and rec.planting.variety else 'N/A'
                field   = rec.planting.field.name   if rec.planting and rec.planting.field   else 'N/A'
                yld_data.append([
                    rec.created_at.strftime('%Y-%m-%d'),
                    variety[:16],
                    field[:20],
                    str(rec.predicted_sacks_per_ha or '-'),
                    str(rec.total_sacks or '-'),
                    rec.harvest_date.strftime('%Y-%m-%d') if rec.harvest_date else '-',
                ])
            yld_table = Table(yld_data, colWidths=[1.4*inch, 1.6*inch, 2*inch, 1.2*inch, 1.2*inch, 1.4*inch])
            yld_table.setStyle(header_style(BLUE))
            elems.append(yld_table)

        doc.build(elems)
        buffer.seek(0)

        fname = f'agriscan_report_{start_date}_{end_date}.pdf'
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{fname}"'
        return response

    messages.error(request, "Invalid export format.")
    return redirect('polls:reports')


@login_required(login_url=reverse_lazy('polls:login'))
def detections_list(request):
    from datetime import timedelta
    
    # Get user profile
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    # Filters
    disease_filter = request.GET.get("disease")
    variety_filter = request.GET.get("variety")
    search = request.GET.get("search", "").strip()
    date_filter = request.GET.get("date_filter")
    sort = request.GET.get("sort", "-severity_pct")
    page = request.GET.get("page", 1)
    _ALLOWED_PAGE_SIZES = {10, 25, 50, 100}
    try:
        page_size = int(request.GET.get("page_size", 25))
    except (ValueError, TypeError):
        page_size = 25
    if page_size not in _ALLOWED_PAGE_SIZES:
        page_size = 25

    # Filter by role: farmers see only their data, technicians/admins see all
    qs = DetectionRecord.objects.filter(is_active=True).select_related("disease", "model_version", "planting__field", "planting__variety")
    qs = filter_queryset_by_role(request, qs)
    
    if disease_filter:
        qs = qs.filter(disease__name__iexact=disease_filter)

    if variety_filter:
        qs = qs.filter(planting__variety__code__iexact=variety_filter)
    
    if search:
        from django.db.models import Q
        pk_q = Q()
        try:
            pk_q = Q(pk=int(search))
        except (ValueError, TypeError):
            pass
        qs = qs.filter(
            pk_q |
            Q(disease__name__icontains=search) |
            Q(planting__variety__code__icontains=search) |
            Q(planting__variety__name__icontains=search) |
            Q(planting__field__name__icontains=search)
        )
    
    if date_filter:
        today = timezone.now().date()
        # BEST PRACTICE: Use timezone-aware date ranges instead of __date lookup
        if date_filter == "today":
            start_dt = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
            end_dt = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))
            qs = qs.filter(created_at__gte=start_dt, created_at__lte=end_dt)
        elif date_filter == "week":
            start_date = today - timedelta(days=7)
            start_dt = timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
            qs = qs.filter(created_at__gte=start_dt)
        elif date_filter == "month":
            start_date = today - timedelta(days=30)
            start_dt = timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
            qs = qs.filter(created_at__gte=start_dt)

    # Allowed sorts
    allowed_sorts = {
        "-created_at", "created_at",
        "severity_pct", "-severity_pct",
        "confidence_pct", "-confidence_pct",
        "pk", "-pk",
        "disease__name", "-disease__name",
        "planting__variety__code", "-planting__variety__code",
        "planting__field__name", "-planting__field__name",
    }
    if sort not in allowed_sorts:
        sort = "-severity_pct"
    qs = qs.order_by(sort)

    paginator = Paginator(qs, page_size)
    try:
        page_obj = paginator.get_page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    query_string = _build_query_string(request)
    page_range = page_obj.paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)

    detection_classes = services.list_detection_classes()
    varieties = [v[0] for v in services.get_variety_choices()]
    context = {
        "detections": page_obj.object_list,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "page_range": page_range,
        "query_string": query_string,
        "total_count": paginator.count,
        "media_url": settings.MEDIA_URL,
        "detection_classes": detection_classes,
        "varieties": varieties,
        "sort_by": sort,
        "page_size": page_size,
    }
    return render(request, "detections/list.html", context)


@login_required(login_url=reverse_lazy('polls:login'))
def detections_detail(request, pk: int):
    """View detailed treatment information for a detection record."""
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    # Check if detection exists first
    try:
        detection = DetectionRecord.objects.get(pk=pk)
    except DetectionRecord.DoesNotExist:
        messages.error(request, f"Detection #{pk} not found.")
        return redirect('polls:detections_list')
    
    # Check if user owns this detection (or is admin/technician who can view all)
    role = user_profile.role if user_profile else 'farmer'
    if detection.user != user_profile and role not in ('admin', 'technician'):
        messages.error(request, "You don't have permission to view this detection.")
        return redirect('polls:detections_list')
    
    # Get detailed treatment information
    detailed_treatment = None
    treatment_obj      = None
    urgency_levels_json = '[]'
    if detection.disease:
        detailed_treatment = services.get_detailed_treatment(
            detection.disease.name,
            detection.severity_pct or 50
        )
        # Also fetch the live ORM object for priority-aware urgency levels
        treatment_obj = services.get_treatment_object(
            detection.disease.name,
            detection.severity_pct or 50
        )
        if treatment_obj:
            import json
            # Serialize urgency levels to JSON for inline <script> use
            # (index 0 = None placeholder → null in JSON)
            raw_levels = treatment_obj.get_urgency_levels()
            urgency_levels_json = json.dumps(
                [None if lvl is None else lvl for lvl in raw_levels],
                ensure_ascii=False,
            )

    # Build factor→action map JSON for the template script block
    factors_with_actions_json = '[]'
    if detailed_treatment and detailed_treatment.get('factors_with_actions'):
        import json as _json
        factors_with_actions_json = _json.dumps(
            detailed_treatment['factors_with_actions'],
            ensure_ascii=False,
        )

    context = {
        'detection': detection,
        'detailed_treatment': detailed_treatment,
        'treatment_obj': treatment_obj,
        'urgency_levels_json': urgency_levels_json,
        'factors_with_actions_json': factors_with_actions_json,
        'media_url': settings.MEDIA_URL,
    }
    return render(request, "detections/detail.html", context)


@login_required(login_url=reverse_lazy('polls:login'))
def detections_edit(request, pk: int):
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    # Check if detection exists first
    try:
        detection = DetectionRecord.objects.get(pk=pk)
    except DetectionRecord.DoesNotExist:
        messages.error(request, f"Detection #{pk} not found.")
        return redirect('polls:detections_list')
    
    # Check ownership or admin/technician role
    role = user_profile.role if user_profile else 'farmer'
    if detection.user != user_profile and role not in ('admin', 'technician'):
        messages.error(request, "You don't have permission to edit this detection.")
        return redirect('polls:detections_list')
    
    old_image = detection.image_path
    form = DetectionRecordForm(request.POST or None, request.FILES or None, instance=detection)
    if request.method == "POST" and form.is_valid():
        detection = form.save(commit=False)
        new_image = form.cleaned_data.get("new_image")
        if new_image:
            services.delete_detection_image(old_image)
            _, rel_path = services.save_detection_image(new_image)
            detection.image_path = str(rel_path)
        if not detection.source:
            detection.source = "manual"
        # Farmers can only change source + image — re-lock AI fields from DB
        if role == 'farmer':
            original = DetectionRecord.objects.get(pk=pk)
            detection.disease         = original.disease
            detection.confidence_pct  = original.confidence_pct
            detection.severity_pct    = original.severity_pct
            detection.model_version   = original.model_version
        detection.save()
        messages.success(request, "Detection updated.")
        return redirect("polls:detections_list")
    return render(
        request,
        "detections/form.html",
        {
            "form": form,
            "is_edit": True,
            "record": detection,
            "media_url": settings.MEDIA_URL,
            "role": role,
        },
    )


@login_required(login_url=reverse_lazy('polls:login'))
def detections_bulk_delete(request):
    """Bulk archive (soft-delete) selected detection records."""
    if request.method != "POST":
        return redirect('polls:detections_list')

    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:detections_list')

    role = user_profile.role if user_profile else 'farmer'
    raw_ids = request.POST.getlist('selected_ids')

    # Parse and validate IDs
    try:
        ids = [int(i) for i in raw_ids if str(i).strip().isdigit()]
    except (ValueError, TypeError):
        messages.error(request, "Invalid selection.")
        return redirect('polls:detections_list')

    if not ids:
        messages.warning(request, "No detections selected.")
        return redirect('polls:detections_list')

    qs = DetectionRecord.objects.filter(pk__in=ids, is_active=True)

    # Farmers can only delete their own; admin/technician can delete any
    if role not in ('admin', 'technician'):
        qs = qs.filter(user=user_profile)

    count = qs.count()
    qs.update(is_active=False)
    messages.success(request, f"📦 {count} detection{'s' if count != 1 else ''} archived successfully.")
    return redirect('polls:detections_list')


@login_required(login_url=reverse_lazy('polls:login'))
def detections_delete(request, pk: int):
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    # Check if detection exists first
    try:
        detection = DetectionRecord.objects.get(pk=pk)
    except DetectionRecord.DoesNotExist:
        messages.error(request, f"Detection #{pk} not found.")
        return redirect('polls:detections_list')
    
    # BEST PRACTICE: Role-based access control
    # Farmers: Can only delete their own detections
    # Admin/Technician: Can delete any detection (for moderation)
    role = user_profile.role if user_profile else 'farmer'
    if detection.user != user_profile and role not in ('admin', 'technician'):
        messages.error(request, "You don't have permission to delete this detection.")
        return redirect('polls:detections_list')
    
    if request.method == "POST":
        detection.is_active = False
        detection.save(update_fields=['is_active'])
        messages.success(request, f"📦 Detection #{pk} archived. Restore it anytime from Trash.")
        return redirect("polls:detections_list")
    return redirect("polls:detections_list")


@login_required(login_url=reverse_lazy('polls:login'))
def yield_records_list(request):
    from datetime import timedelta
    
    # Get user profile
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    variety_filter = request.GET.get("variety")
    search = request.GET.get("search", "").strip()
    date_filter = request.GET.get("date_filter")
    sort = request.GET.get("sort", "-predicted_yield_tons_per_ha")
    page = request.GET.get("page", 1)
    _ALLOWED_PAGE_SIZES = {10, 25, 50, 100}
    try:
        page_size = int(request.GET.get("page_size", 25))
    except (ValueError, TypeError):
        page_size = 25
    if page_size not in _ALLOWED_PAGE_SIZES:
        page_size = 25

    # Filter by role: farmers see only their data, technicians/admins see all.
    # A yield record belongs to a farmer when:
    #   (a) planting__field__owner = farmer profile, OR
    #   (b) planting is NULL but detection__planting__field__owner = farmer profile
    #       (created via detection path without a separate planting FK), OR
    #   (c) planting is NULL AND detection is NULL (pure manual entry) — these
    #       records have no ownership anchor; show them only to admins/technicians.
    qs = YieldPrediction.objects.filter(is_active=True).select_related(
        "detection", "detection__planting__field",
        "planting__variety", "planting__field",
    )
    role = user_profile.role if user_profile else 'farmer'
    if role not in ('admin', 'technician'):
        from django.db.models import Q
        qs = qs.filter(
            Q(planting__field__owner=user_profile) |
            Q(planting__isnull=True, detection__planting__field__owner=user_profile)
        )
    
    if variety_filter:
        qs = qs.filter(planting__variety__code__iexact=variety_filter)
    
    if search:
        from django.db.models import Q
        pk_q = Q()
        try:
            pk_q = Q(pk=int(search))
        except (ValueError, TypeError):
            pass
        qs = qs.filter(
            pk_q |
            Q(planting__variety__name__icontains=search) |
            Q(planting__variety__code__icontains=search) |
            Q(planting__field__name__icontains=search)
        )
    
    if date_filter:
        today = timezone.now().date()
        # BEST PRACTICE: Use timezone-aware date ranges instead of __date lookup
        if date_filter == "today":
            start_dt = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
            end_dt = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.max.time()))
            qs = qs.filter(created_at__gte=start_dt, created_at__lte=end_dt)
        elif date_filter == "week":
            start_date = today - timedelta(days=7)
            start_dt = timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
            qs = qs.filter(created_at__gte=start_dt)
        elif date_filter == "month":
            start_date = today - timedelta(days=30)
            start_dt = timezone.make_aware(timezone.datetime.combine(start_date, timezone.datetime.min.time()))
            qs = qs.filter(created_at__gte=start_dt)

    allowed_sorts = {
        "-created_at", "created_at",
        "predicted_sacks_per_ha", "-predicted_sacks_per_ha",
        "predicted_yield_tons_per_ha", "-predicted_yield_tons_per_ha",
        "predicted_total_production_tons", "-predicted_total_production_tons",
        "estimated_harvest_date", "-estimated_harvest_date",
        "planting__planting_date", "-planting__planting_date",
        "pk", "-pk",
        "planting__variety__code", "-planting__variety__code",
        "planting__field__name", "-planting__field__name",
    }
    if sort not in allowed_sorts:
        sort = "-predicted_yield_tons_per_ha"
    qs = qs.order_by(sort)

    paginator = Paginator(qs, page_size)
    try:
        page_obj = paginator.get_page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    query_string = _build_query_string(request)
    page_range = page_obj.paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)

    varieties = [v[0] for v in services.get_variety_choices()]
    context = {
        "records": page_obj.object_list,
        "page_obj": page_obj,
        "is_paginated": page_obj.has_other_pages(),
        "page_range": page_range,
        "query_string": query_string,
        "total_count": paginator.count,
        "varieties": varieties,
        "sort_by": sort,
        "page_size": page_size,
    }
    return render(request, "yields/list.html", context)


@login_required(login_url=reverse_lazy('polls:login'))
def yield_record_edit(request, pk: int):
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    # BEST PRACTICE: Role-based access control
    # Farmers: Can only edit their own yield records.
    # A record is "owned" by the farmer if:
    #   (a) planting__field__owner matches, OR
    #   (b) planting is NULL but the record was created from the farmer's
    #       detection (detection__planting__field__owner).
    # Using a broad pk lookup + Python ownership check avoids the 404 that
    # occurs when planting=NULL makes the ORM join return no rows.
    if user_profile.role == 'farmer':
        record = get_object_or_404(YieldPrediction, pk=pk)
        owned = False
        if record.planting and record.planting.field and record.planting.field.owner == user_profile:
            owned = True
        elif record.detection and record.detection.planting and record.detection.planting.field and record.detection.planting.field.owner == user_profile:
            owned = True
        if not owned:
            messages.error(request, "You do not have permission to edit this record.")
            return redirect('polls:yield_records_list')
    else:
        # Admin/Technician can access all records
        record = get_object_or_404(YieldPrediction, pk=pk)
    
    form = YieldPredictionRecordForm(request.POST or None, instance=record)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Yield record updated.")
        return redirect("polls:yield_records_list")
    return render(request, "yields/form.html", {"form": form, "is_edit": True, "record": record})


@login_required(login_url=reverse_lazy('polls:login'))
def yield_records_bulk_delete(request):
    if request.method != "POST":
        return redirect('polls:yield_records_list')
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:yield_records_list')
    role = user_profile.role
    raw_ids = request.POST.getlist('selected_ids')
    try:
        ids = [int(i) for i in raw_ids if str(i).strip().isdigit()]
    except (ValueError, TypeError):
        messages.error(request, "Invalid selection.")
        return redirect('polls:yield_records_list')
    if not ids:
        messages.warning(request, "No records selected.")
        return redirect('polls:yield_records_list')
    from django.db.models import Q
    qs = YieldPrediction.objects.filter(pk__in=ids, is_active=True)
    if role not in ('admin', 'technician'):
        qs = qs.filter(
            Q(planting__field__owner=user_profile) |
            Q(detection__planting__field__owner=user_profile)
        )
    count = qs.count()
    qs.update(is_active=False)
    messages.success(request, f"📦 {count} yield record{'s' if count != 1 else ''} archived successfully.")
    return redirect('polls:yield_records_list')


@login_required(login_url=reverse_lazy('polls:login'))
def yield_record_delete(request, pk: int):
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    # BEST PRACTICE: Role-based access control
    # Farmers: Can only delete their own yield records.
    # Same ownership logic as yield_record_edit — planting may be NULL.
    if user_profile.role == 'farmer':
        record = get_object_or_404(YieldPrediction, pk=pk)
        owned = False
        if record.planting and record.planting.field and record.planting.field.owner == user_profile:
            owned = True
        elif record.detection and record.detection.planting and record.detection.planting.field and record.detection.planting.field.owner == user_profile:
            owned = True
        if not owned:
            messages.error(request, "You do not have permission to delete this record.")
            return redirect('polls:yield_records_list')
    else:
        # Admin/Technician can access all records
        record = get_object_or_404(YieldPrediction, pk=pk)
    
    if request.method == "POST":
        record.is_active = False
        record.save(update_fields=['is_active'])
        messages.success(request, f"📦 Yield record #{pk} archived. Restore it anytime from Trash.")
        return redirect("polls:yield_records_list")
    return redirect("polls:yield_records_list")


@login_required(login_url=reverse_lazy('polls:login'))
def export_detections_csv(request):
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')

    from datetime import datetime as _dt
    ALL_COLS = ['id', 'date', 'disease', 'confidence', 'severity', 'field', 'source', 'model']
    selected_cols = set(request.GET.getlist('cols')) or set(ALL_COLS)

    # Optional date range
    start_str = request.GET.get('start_date', '')
    end_str   = request.GET.get('end_date', '')
    try:
        start_dt = timezone.make_aware(_dt.strptime(start_str, '%Y-%m-%d'))
        end_dt   = timezone.make_aware(_dt.strptime(end_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59))
    except ValueError:
        start_dt = end_dt = None

    detections_qs = DetectionRecord.objects.filter(is_active=True).select_related(
        'disease', 'model_version', 'planting__field'
    ).order_by('-created_at')
    detections_qs = filter_queryset_by_role(request, detections_qs)
    if start_dt and end_dt:
        detections_qs = detections_qs.filter(created_at__gte=start_dt, created_at__lte=end_dt)
    total = detections_qs.count()

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    date_tag = f'{start_str}_to_{end_str}' if start_str and end_str else timezone.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="detections_{date_tag}.csv"'

    writer = csv.writer(response)
    writer.writerow(['AgriScan+ Detection Records'])
    writer.writerow(['Generated',   timezone.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow(['Exported By', request.user.get_full_name() or request.user.username])
    if start_str and end_str:
        writer.writerow(['Date Range', f'{start_str} to {end_str}'])
    writer.writerow(['Total Records', total])
    writer.writerow([])

    COL_LABELS = {
        'id': 'ID', 'date': 'Date', 'disease': 'Disease',
        'confidence': 'Confidence (%)', 'severity': 'Severity (%)',
        'field': 'Field', 'source': 'Source', 'model': 'Model Version',
    }
    writer.writerow([COL_LABELS[c] for c in ALL_COLS if c in selected_cols])

    for det in detections_qs:
        field_name = det.planting.field.name if det.planting and det.planting.field else 'N/A'
        row_map = {
            'id':         det.pk,
            'date':       det.created_at.strftime('%Y-%m-%d %H:%M'),
            'disease':    det.disease.name if det.disease else 'Healthy',
            'confidence': round(float(det.confidence_pct or 0), 2),
            'severity':   round(float(det.severity_pct or 0), 1) if det.severity_pct else '',
            'field':      field_name,
            'source':     det.source or '',
            'model':      det.model_version.version if det.model_version else '',
        }
        writer.writerow([row_map[c] for c in ALL_COLS if c in selected_cols])

    return response


@login_required(login_url=reverse_lazy('polls:login'))
def export_yields_csv(request):
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')

    from datetime import datetime as _dt
    ALL_COLS = ['id', 'date', 'variety', 'field', 'sacks_per_ha', 'confidence', 'area', 'total_sacks', 'total_tons', 'harvest_date']
    selected_cols = set(request.GET.getlist('cols')) or set(ALL_COLS)

    # Optional date range
    start_str = request.GET.get('start_date', '')
    end_str   = request.GET.get('end_date', '')
    try:
        start_dt = timezone.make_aware(_dt.strptime(start_str, '%Y-%m-%d'))
        end_dt   = timezone.make_aware(_dt.strptime(end_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59))
    except ValueError:
        start_dt = end_dt = None

    records_qs = YieldPrediction.objects.filter(is_active=True).select_related(
        'planting__field', 'planting__variety'
    ).order_by('-created_at')
    records_qs = filter_queryset_by_role(request, records_qs, user_field="planting__field__owner")
    if start_dt and end_dt:
        records_qs = records_qs.filter(created_at__gte=start_dt, created_at__lte=end_dt)
    total = records_qs.count()

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    date_tag = f'{start_str}_to_{end_str}' if start_str and end_str else timezone.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="yield_records_{date_tag}.csv"'

    writer = csv.writer(response)
    writer.writerow(['AgriScan+ Yield Prediction Records'])
    writer.writerow(['Generated',   timezone.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow(['Exported By', request.user.get_full_name() or request.user.username])
    if start_str and end_str:
        writer.writerow(['Date Range', f'{start_str} to {end_str}'])
    writer.writerow(['Total Records', total])
    writer.writerow([])

    COL_LABELS = {
        'id': 'ID', 'date': 'Date', 'variety': 'Variety', 'field': 'Field',
        'sacks_per_ha': 'Sacks/ha', 'confidence': 'Confidence (%)',
        'area': 'Area (ha)', 'total_sacks': 'Total Sacks',
        'total_tons': 'Total Tons', 'harvest_date': 'Harvest Date',
    }
    writer.writerow([COL_LABELS[c] for c in ALL_COLS if c in selected_cols])

    for rec in records_qs:
        variety = rec.planting.variety.code if rec.planting and rec.planting.variety else 'N/A'
        field   = rec.planting.field.name   if rec.planting and rec.planting.field   else 'N/A'
        row_map = {
            'id':           rec.pk,
            'date':         rec.created_at.strftime('%Y-%m-%d %H:%M'),
            'variety':      variety,
            'field':        field,
            'sacks_per_ha': rec.predicted_sacks_per_ha or '',
            'confidence':   round(float(rec.confidence_pct or 0), 2) if rec.confidence_pct else '',
            'area':         rec.area_hectares or '',
            'total_sacks':  rec.total_sacks or '',
            'total_tons':   rec.total_tons or '',
            'harvest_date': rec.harvest_date.strftime('%Y-%m-%d') if rec.harvest_date else '',
        }
        writer.writerow([row_map[c] for c in ALL_COLS if c in selected_cols])

    return response


@login_required(login_url=reverse_lazy('polls:login'))
def export_detections_pdf(request):
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')

    from datetime import datetime as _dt
    start_str = request.GET.get('start_date', '')
    end_str   = request.GET.get('end_date', '')
    try:
        start_dt = timezone.make_aware(_dt.strptime(start_str, '%Y-%m-%d'))
        end_dt   = timezone.make_aware(_dt.strptime(end_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59))
    except ValueError:
        start_dt = end_dt = None

    detections_qs = DetectionRecord.objects.filter(is_active=True).select_related(
        'disease', 'planting__field'
    ).order_by('-created_at')
    detections_qs = filter_queryset_by_role(request, detections_qs)
    if start_dt and end_dt:
        detections_qs = detections_qs.filter(created_at__gte=start_dt, created_at__lte=end_dt)
    detections = list(detections_qs)
    total = len(detections)

    GREEN = colors.HexColor('#16a34a')
    LGRAY = colors.HexColor('#f3f4f6')

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=landscape(A4),
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
    )
    styles = getSampleStyleSheet()
    elems = []

    # Cover
    elems.append(Paragraph('<b>AgriScan+ Detection Records Report</b>', styles['Title']))
    cover_line = (
        f'Generated: {timezone.now().strftime("%B %d, %Y %H:%M")} &nbsp;|&nbsp; '
        f'By: {request.user.get_full_name() or request.user.username} &nbsp;|&nbsp; '
        f'Total: {total} records'
    )
    if start_str and end_str:
        cover_line += f' &nbsp;|&nbsp; Date Range: {start_str} to {end_str}'
    elems.append(Paragraph(cover_line, styles['Normal']))
    elems.append(Spacer(1, 0.3*inch))

    data = [['ID', 'Date', 'Disease', 'Confidence', 'Severity', 'Field']]
    for det in detections:
        field_name = det.planting.field.name if det.planting and det.planting.field else 'N/A'
        data.append([
            str(det.pk),
            det.created_at.strftime('%Y-%m-%d'),
            (det.disease.name if det.disease else 'Healthy')[:24],
            f"{round(float(det.confidence_pct or 0), 1)}%",
            f"{round(float(det.severity_pct or 0), 1)}%" if det.severity_pct else '-',
            field_name[:26],
        ])

    table = Table(data, colWidths=[0.7*inch, 1.3*inch, 2.2*inch, 1.2*inch, 1.2*inch, 2.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND',     (0, 0), (-1, 0), GREEN),
        ('TEXTCOLOR',      (0, 0), (-1, 0), colors.white),
        ('FONTNAME',       (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',       (0, 0), (-1, 0), 9),
        ('FONTSIZE',       (0, 1), (-1, -1), 8),
        ('ALIGN',          (0, 0), (-1, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LGRAY]),
        ('GRID',           (0, 0), (-1, -1), 0.4, colors.HexColor('#d1d5db')),
        ('TOPPADDING',     (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING',  (0, 0), (-1, -1), 4),
        ('LEFTPADDING',    (0, 0), (-1, -1), 6),
    ]))
    elems.append(table)

    doc.build(elems)
    buffer.seek(0)
    date_tag = f'{start_str}_to_{end_str}' if start_str and end_str else timezone.now().strftime('%Y%m%d_%H%M%S')
    fname = f'detections_report_{date_tag}.pdf'
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{fname}"'
    return response


@login_required(login_url=reverse_lazy('polls:login'))
def export_yields_pdf(request):
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')

    from datetime import datetime as _dt
    start_str = request.GET.get('start_date', '')
    end_str   = request.GET.get('end_date', '')
    try:
        start_dt = timezone.make_aware(_dt.strptime(start_str, '%Y-%m-%d'))
        end_dt   = timezone.make_aware(_dt.strptime(end_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59))
    except ValueError:
        start_dt = end_dt = None

    records_qs = YieldPrediction.objects.filter(is_active=True).select_related(
        'planting__field', 'planting__variety'
    ).order_by('-created_at')
    records_qs = filter_queryset_by_role(request, records_qs, user_field="planting__field__owner")
    if start_dt and end_dt:
        records_qs = records_qs.filter(created_at__gte=start_dt, created_at__lte=end_dt)
    records = list(records_qs)
    total = len(records)

    BLUE  = colors.HexColor('#1e40af')
    LGRAY = colors.HexColor('#f3f4f6')

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=landscape(A4),
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm,
    )
    styles = getSampleStyleSheet()
    elems = []

    # Cover
    elems.append(Paragraph('<b>AgriScan+ Yield Prediction Report</b>', styles['Title']))
    cover_line = (
        f'Generated: {timezone.now().strftime("%B %d, %Y %H:%M")} &nbsp;|&nbsp; '
        f'By: {request.user.get_full_name() or request.user.username} &nbsp;|&nbsp; '
        f'Total: {total} records'
    )
    if start_str and end_str:
        cover_line += f' &nbsp;|&nbsp; Date Range: {start_str} to {end_str}'
    elems.append(Paragraph(cover_line, styles['Normal']))
    elems.append(Spacer(1, 0.3*inch))

    data = [['ID', 'Date', 'Variety', 'Field', 'Sacks/ha', 'Area (ha)', 'Total Sacks', 'Harvest Date']]
    for rec in records:
        variety = rec.planting.variety.code if rec.planting and rec.planting.variety else 'N/A'
        field   = rec.planting.field.name   if rec.planting and rec.planting.field   else 'N/A'
        data.append([
            str(rec.pk),
            rec.created_at.strftime('%Y-%m-%d'),
            variety[:16],
            field[:20],
            str(rec.predicted_sacks_per_ha or '-'),
            str(rec.area_hectares or '-'),
            str(rec.total_sacks or '-'),
            rec.harvest_date.strftime('%Y-%m-%d') if rec.harvest_date else '-',
        ])

    table = Table(data, colWidths=[0.6*inch, 1.2*inch, 1.3*inch, 1.8*inch, 1.1*inch, 1.1*inch, 1.2*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND',     (0, 0), (-1, 0), BLUE),
        ('TEXTCOLOR',      (0, 0), (-1, 0), colors.white),
        ('FONTNAME',       (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',       (0, 0), (-1, 0), 9),
        ('FONTSIZE',       (0, 1), (-1, -1), 8),
        ('ALIGN',          (0, 0), (-1, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LGRAY]),
        ('GRID',           (0, 0), (-1, -1), 0.4, colors.HexColor('#d1d5db')),
        ('TOPPADDING',     (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING',  (0, 0), (-1, -1), 4),
        ('LEFTPADDING',    (0, 0), (-1, -1), 6),
    ]))
    elems.append(table)

    doc.build(elems)
    buffer.seek(0)
    fname = f'yield_report_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{fname}"'
    return response


# ============================================================================
# FIELD MANAGEMENT VIEWS
# ============================================================================

@login_required(login_url=reverse_lazy('polls:login'))
def fields_list(request):
    """
    List fields based on user role:
    - Farmers: See only their own fields
    - Technicians/Admins: See ALL fields (to help manage farmers)
    """
    from .models import Field
    from django.utils import timezone
    from django.db.models import Q, Exists, OuterRef
    
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    role = user_profile.role
    today = timezone.now().date()
    
    # Annotate fields with whether they have active plantings
    from .models import PlantingRecord

    # Tagalog: Ang field ay may active planting kung
    # ang status ay planned o ongoing pa —
    # hindi na kailangang tingnan ang expected_harvest_date.
    # Kapag harvested, failed, o cancelled na,
    # hindi na considered na active.
    active_plantings = PlantingRecord.objects.filter(
        field=OuterRef('pk'),
        status__in=['planned', 'ongoing'],
        is_active=True,
    )
    
    # Role-based filtering
    if role in ['admin', 'technician']:
        # Admin and Technician can see ALL fields
        fields = Field.objects.filter(is_active=True)
    else:
        # Farmers see only their own fields
        fields = Field.objects.filter(owner=user_profile, is_active=True)
    
    # Note: 'barangay' is now CharField, not ForeignKey - removed from select_related
    fields = fields.select_related('owner', 'owner__user').annotate(
        has_active_planting=Exists(active_plantings)
    ).order_by('-created_at')
    
    # Search functionality
    search = request.GET.get('search', '').strip()
    if search:
        pk_q = Q()
        try:
            pk_q = Q(pk=int(search))
        except (ValueError, TypeError):
            pass
        fields = fields.filter(
            pk_q |
            Q(name__icontains=search) |
            Q(barangay__icontains=search) |
            Q(municipality__icontains=search) |
            Q(owner__user__username__icontains=search) |
            Q(owner__user__first_name__icontains=search) |
            Q(owner__user__last_name__icontains=search)
        )

    # Filter by location
    barangay_filter = request.GET.get('barangay', '').strip()
    if barangay_filter:
        fields = fields.filter(barangay__icontains=barangay_filter)

    municipality_filter = request.GET.get('municipality', '').strip()
    if municipality_filter:
        fields = fields.filter(municipality__icontains=municipality_filter)

    # Sort functionality
    sort_by = request.GET.get('sort', '-created_at')
    allowed_sorts = {
        '-created_at', 'created_at',
        'name', '-name',
        'barangay', '-barangay',
        'area_hectares', '-area_hectares',
        'pk', '-pk',
    }
    if sort_by not in allowed_sorts:
        sort_by = '-created_at'
    fields = fields.order_by(sort_by)

    # Pagination
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    allowed_page_sizes = [10, 20, 50, 100]
    try:
        page_size = int(request.GET.get('page_size', 20))
    except (TypeError, ValueError):
        page_size = 20
    if page_size not in allowed_page_sizes:
        page_size = 20

    page = request.GET.get('page', 1)
    total_count = fields.count()

    paginator = Paginator(fields, page_size)
    fields_page = paginator.get_page(page)
    query_string = _build_query_string(request)

    context = {
        'fields': fields_page,
        'page_obj': fields_page,
        'paginator': paginator,
        'is_paginated': fields_page.has_other_pages(),
        'page_range': fields_page.paginator.get_elided_page_range(fields_page.number, on_each_side=1, on_ends=1),
        'total_count': total_count,
        'total_area': sum(f.area_hectares for f in fields if f.area_hectares),
        'today': today,
        'role': role,
        'search': search,
        'barangay_filter': barangay_filter,
        'municipality_filter': municipality_filter,
        'sort_by': sort_by,
        'page_size': page_size,
        'allowed_page_sizes': allowed_page_sizes,
        'query_string': query_string,
    }
    return render(request, 'fields/list.html', context)


@login_required(login_url=reverse_lazy('polls:login'))
def field_create(request):
    """
    Create a new field.
    BEST PRACTICE: Admin/Technician can select owner, Farmer creates for themselves.
    """
    from .forms import FieldForm
    
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    role = user_profile.role
    
    if request.method == 'POST':
        form = FieldForm(request.POST, user=request.user)
        if form.is_valid():
            field = form.save(commit=False)
            
            # Set owner based on role
            if role in ['admin', 'technician']:
                # Admin/Technician: Use selected owner from form
                field.owner = form.cleaned_data['owner']
            else:
                # Farmer: Always use their own profile
                field.owner = user_profile
            
            field.save()
            
            # Success message with owner info for admin/technician
            if role in ['admin', 'technician']:
                owner_name = field.owner.user.get_full_name() or field.owner.user.username
                messages.success(request, f"Field '{field.name}' created for {owner_name}!")
            else:
                messages.success(request, f"Field '{field.name}' created successfully!")
            
            return redirect('polls:fields_list')
    else:
        form = FieldForm(user=request.user)
    
    context = {
        'form': form,
        'is_edit': False,
        'role': role,
    }
    return render(request, 'fields/form.html', context)


@login_required(login_url=reverse_lazy('polls:login'))
def field_edit(request, pk: int):
    """
    Edit an existing field.
    - Farmers: Can only edit their own fields
    - Technicians/Admins: Can edit ANY field (to help farmers)
    """
    from .forms import FieldForm
    from .models import Field
    
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    role = user_profile.role
    
    # Role-based access control
    if role in ['admin', 'technician']:
        # Admin/Technician can edit any field
        field = get_object_or_404(Field, pk=pk)
    else:
        # Farmers can only edit their own fields
        field = get_object_or_404(Field, pk=pk, owner=user_profile)
    
    if request.method == 'POST':
        form = FieldForm(request.POST, instance=field, user=request.user)
        if form.is_valid():
            updated_field = form.save(commit=False)
            
            # Handle owner change for admin/technician
            if role in ['admin', 'technician'] and 'owner' in form.cleaned_data:
                updated_field.owner = form.cleaned_data['owner']
            
            updated_field.save()
            
            # Success message with owner info
            if role in ['admin', 'technician']:
                owner_name = updated_field.owner.user.get_full_name() or updated_field.owner.user.username
                messages.success(request, f"Field '{updated_field.name}' updated! (Owner: {owner_name})")
            else:
                messages.success(request, f"Field '{updated_field.name}' updated successfully!")
            
            return redirect('polls:fields_list')
    else:
        form = FieldForm(instance=field, user=request.user)
    
    context = {
        'form': form,
        'is_edit': True,
        'field': field,
        'role': role,
    }
    return render(request, 'fields/form.html', context)


@login_required(login_url=reverse_lazy('polls:login'))
def field_delete(request, pk: int):
    """
    Delete a field.
    - Farmers: Can only delete their own fields
    - Technicians/Admins: Can delete ANY field (to help manage system)
    """
    from .models import Field
    
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    role = user_profile.role
    
    # Role-based access control
    if role in ['admin', 'technician']:
        # Admin/Technician can delete any field
        field = get_object_or_404(Field, pk=pk)
    else:
        # Farmers can only delete their own fields
        field = get_object_or_404(Field, pk=pk, owner=user_profile)
    
    if request.method == 'POST':
        field_name = field.name
        field.delete()
        messages.success(request, f"📦 Field '{field_name}' archived. Restore it anytime from Trash.")
        return redirect('polls:fields_list')
    return redirect('polls:fields_list')


# ============================================================================
# PLANTING RECORD MANAGEMENT VIEWS
# ============================================================================

@login_required(login_url=reverse_lazy('polls:login'))
def plantings_list(request):
    """
    List planting records based on user role:
    - Farmers: See only their own plantings
    - Technicians/Admins: See ALL plantings (to monitor all farms)
    """
    from .models import PlantingRecord
    from django.utils import timezone
    
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    role = user_profile.role
    
    # Role-based filtering
    if role in ['admin', 'technician']:
        # Admin and Technician can see ALL plantings
        plantings = PlantingRecord.objects.filter(is_active=True)
    else:
        # Farmers see only their own plantings
        plantings = PlantingRecord.objects.filter(field__owner=user_profile, is_active=True)
    
    plantings = plantings.select_related(
        'field', 'field__owner', 'field__owner__user', 'variety'
    ).order_by('-planting_date')
    
    # Search functionality
    search = request.GET.get('search', '').strip()
    variety_filter = request.GET.get('variety', '').strip()
    season_filter = request.GET.get('season', '').strip()
    status_filter = request.GET.get('status', '').strip()
    field_filter = request.GET.get('field', '').strip()

    if variety_filter:
        plantings = plantings.filter(variety__code__iexact=variety_filter)

    if season_filter:
        plantings = plantings.filter(season__iexact=season_filter)

    if status_filter:
        plantings = plantings.filter(status__iexact=status_filter)

    if field_filter:
        # allow searching by field id or name
        try:
            field_pk = int(field_filter)
            plantings = plantings.filter(field__pk=field_pk)
        except (ValueError, TypeError):
            plantings = plantings.filter(field__name__icontains=field_filter)

    if search:
        from django.db.models import Q
        pk_q = Q()
        try:
            pk_q = Q(pk=int(search))
        except (ValueError, TypeError):
            pass
        plantings = plantings.filter(
            pk_q |
            Q(field__name__icontains=search) |
            Q(field__barangay__icontains=search) |
            Q(field__municipality__icontains=search) |
            Q(season__icontains=search) |
            Q(status__icontains=search) |
            Q(variety__name__icontains=search) |
            Q(variety__code__icontains=search) |
            Q(field__owner__user__username__icontains=search) |
            Q(field__owner__user__first_name__icontains=search) |
            Q(field__owner__user__last_name__icontains=search)
        )

    # Sort functionality
    sort_by = request.GET.get('sort', '-planting_date')
    allowed_sorts = {
        '-planting_date', 'planting_date',
        'field__name', '-field__name',
        'variety__code', '-variety__code',
        'expected_harvest_date', '-expected_harvest_date',
        'pk', '-pk',
    }
    if sort_by not in allowed_sorts:
        sort_by = '-planting_date'
    plantings = plantings.order_by(sort_by)

    # Pagination with configurable page size
    allowed_page_sizes = [10, 20, 50, 100]
    try:
        page_size = int(request.GET.get('page_size', 20))
    except (TypeError, ValueError):
        page_size = 20
    if page_size not in allowed_page_sizes:
        page_size = 20

    page = request.GET.get('page', 1)
    total_count = plantings.count()

    paginator = Paginator(plantings, page_size)
    plantings_page = paginator.get_page(page)

    query_string = _build_query_string(request)
    varieties = [v[0] for v in services.get_variety_choices()]
    context = {
        'plantings': plantings_page,
        'page_obj': plantings_page,
        'paginator': paginator,
        'is_paginated': plantings_page.has_other_pages(),
        'page_range': plantings_page.paginator.get_elided_page_range(plantings_page.number, on_each_side=1, on_ends=1),
        'total_count': total_count,
        'page_size': page_size,
        'allowed_page_sizes': allowed_page_sizes,
        'query_string': query_string,
        'today': timezone.now().date(),
        'role': role,
        'search': search,
        'variety_filter': variety_filter,
        'season_filter': season_filter,
        'status_filter': status_filter,
        'field_filter': field_filter,
        'varieties': varieties,
        'sort_by': sort_by,
    }
    return render(request, 'plantings/list.html', context)


@login_required(login_url=reverse_lazy('polls:login'))
def planting_create(request):
    """Create a new planting record."""
    from .forms import PlantingRecordForm

    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')

    role = user_profile.role
    is_staff = role in ('admin', 'technician')

    # Admin/Tech: support owner filter (change_owner pattern)
    if is_staff:
        from .models import Profile as ProfileModel
        profile_id = request.POST.get('profile_id') or request.GET.get('profile_id')
        try:
            target_profile = ProfileModel.objects.get(pk=profile_id) if profile_id else None
        except ProfileModel.DoesNotExist:
            target_profile = None
    else:
        target_profile = None

    if request.method == 'POST':
        # If admin changed the owner dropdown, reload with filtered fields — don't save yet
        if is_staff and request.POST.get('change_owner') == '1':
            form = PlantingRecordForm(user=request.user, target_profile=target_profile)

            # Compute crop counts per field for current year (3-crop max)
            # Includes ALL statuses (harvested/failed/cancelled/archived) like PlantingRecord.save().
            from .models import PlantingRecord
            from django.db.models import Count
            import json

            year = timezone.now().year
            field_qs = form.fields['field'].queryset
            field_ids = list(field_qs.values_list('pk', flat=True))
            counts = PlantingRecord.objects.filter(
                field_id__in=field_ids,
                planting_date__year=year,
            ).values('field_id').annotate(count=Count('pk'))

            mapping = {str(fid): 0 for fid in field_ids}
            for row in counts:
                mapping[str(row['field_id'])] = row['count']
            field_crop_counts_json = json.dumps(mapping)

            # Attach to form render so template can use it without complex template calls
            form.fields['field'].widget.attrs['data-crop-counts'] = field_crop_counts_json

            context = {
                'form': form,
                'is_edit': False,
                'is_staff': is_staff,
                'target_profile': target_profile,
                'allowed_past_days_planting': services.get_allowed_past_days_for_planting(),
                'today': timezone.now().date(),
                'field_crop_counts_json': field_crop_counts_json,
            }
            return render(request, 'plantings/form.html', context)

        form = PlantingRecordForm(request.POST, user=request.user, target_profile=target_profile)
        if form.is_valid():
            from django.core.exceptions import ValidationError
            try:
                planting = form.save()
                messages.success(request, f"Planting record for '{planting.field.name}' created successfully!")
                return redirect('polls:plantings_list')
            except ValidationError as e:
                # Surface model validation errors (e.g., max 3 cycles per year) on the form
                if hasattr(e, 'message_dict'):
                    for field, msgs in e.message_dict.items():
                        for msg in msgs:
                            form.add_error(field, msg)
                else:
                    form.add_error(None, e.messages)
    else:
        form = PlantingRecordForm(user=request.user, target_profile=target_profile)

    # Compute crop counts per field for current year (3-crop max).
    # Includes ALL statuses (harvested/failed/cancelled/archived) like PlantingRecord.save().
    from .models import PlantingRecord
    from django.db.models import Count
    import json

    year = timezone.now().year
    field_qs = form.fields['field'].queryset
    field_ids = list(field_qs.values_list('pk', flat=True))
    counts = PlantingRecord.objects.filter(
        field_id__in=field_ids,
        planting_date__year=year,
    ).values('field_id').annotate(count=Count('pk'))

    mapping = {str(fid): 0 for fid in field_ids}
    for row in counts:
        mapping[str(row['field_id'])] = row['count']
    field_crop_counts_json = json.dumps(mapping)

    # Attach to form field widget attrs so template can use it without invoking as_widget()
    form.fields['field'].widget.attrs['data-crop-counts'] = field_crop_counts_json

    context = {
        'form': form,
        'is_edit': False,
        'is_staff': is_staff,
        'target_profile': target_profile,
        'allowed_past_days_planting': services.get_allowed_past_days_for_planting(),
        'detection_confidence_threshold': services.get_detection_confidence_threshold(),
        'today': timezone.now().date(),
        'field_crop_counts_json': field_crop_counts_json,
    }
    return render(request, 'plantings/form.html', context)


@login_required(login_url=reverse_lazy('polls:login'))
def planting_edit(request, pk: int):
    """
    Edit an existing planting record.
    - Farmers: Can only edit their own plantings
    - Technicians/Admins: Can edit ANY planting (to correct data)
    """
    from .forms import PlantingRecordForm
    from .models import PlantingRecord
    
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    role = user_profile.role
    
    # Role-based access control
    if role in ['admin', 'technician']:
        # Admin/Technician can edit any planting
        planting = get_object_or_404(PlantingRecord, pk=pk)
    else:
        # Farmers can only edit their own plantings
        planting = get_object_or_404(PlantingRecord, pk=pk, field__owner=user_profile)
    
    if request.method == 'POST':
        form = PlantingRecordForm(request.POST, instance=planting, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Planting record for '{planting.field.name}' updated successfully!")
            return redirect('polls:plantings_list')
    else:
        form = PlantingRecordForm(instance=planting, user=request.user)
    
    context = {
        'form': form,
        'is_edit': True,
        'planting': planting,
        'allowed_past_days_planting': services.get_allowed_past_days_for_planting(),
        'detection_confidence_threshold': services.get_detection_confidence_threshold(),
        'today': timezone.now().date(),
    }
    return render(request, 'plantings/form.html', context)


@login_required(login_url=reverse_lazy('polls:login'))
def planting_delete(request, pk: int):
    """
    Delete a planting record.
    - Farmers: Can only delete their own plantings
    - Technicians/Admins: Can delete ANY planting (to clean up data)
    """
    from .models import PlantingRecord
    
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')
    
    role = user_profile.role
    
    # Role-based access control
    if role in ['admin', 'technician']:
        # Admin/Technician can delete any planting
        planting = get_object_or_404(PlantingRecord, pk=pk)
    else:
        # Farmers can only delete their own plantings
        planting = get_object_or_404(PlantingRecord, pk=pk, field__owner=user_profile)
    
    if request.method == 'POST':
        field_name = planting.field.name
        planting.delete()
        messages.success(request, f"📦 Planting record for field '{field_name}' archived. Restore it anytime from Trash.")
        return redirect('polls:plantings_list')
    return redirect('polls:plantings_list')


# ============================================================================
# HARVEST RECORD MANAGEMENT VIEWS
# ============================================================================

@login_required(login_url=reverse_lazy('polls:login'))
def harvests_list(request):
    """List harvest records with filtering and role-based access."""
    from datetime import date

    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')

    role = user_profile.role
    qs = HarvestRecord.objects.select_related(
        'planting', 'planting__field', 'planting__variety'
    ).filter(is_active=True).order_by('-harvest_date')

    if role not in ['admin', 'technician']:
        qs = qs.filter(planting__field__owner=user_profile)

    # Filters
    search = request.GET.get('search', '').strip()
    field_filter = request.GET.get('field', '').strip()
    variety_filter = request.GET.get('variety', '').strip()
    season_filter = request.GET.get('season', '').strip()
    year_filter = request.GET.get('year', '').strip()

    if field_filter:
        try:
            field_pk = int(field_filter)
            qs = qs.filter(planting__field__pk=field_pk)
        except (ValueError, TypeError):
            qs = qs.filter(planting__field__name__icontains=field_filter)

    if variety_filter:
        qs = qs.filter(planting__variety__code__iexact=variety_filter)

    if season_filter:
        qs = qs.filter(planting__season__iexact=season_filter)

    if year_filter:
        try:
            year = int(year_filter)
            qs = qs.filter(harvest_date__year=year)
        except (ValueError, TypeError):
            pass

    if search:
        from django.db.models import Q
        pk_q = Q()
        year_q = Q()
        try:
            pk_q = Q(pk=int(search))
            # If the user types a year (e.g. 2024), match harvest_date year
            year_q = Q(harvest_date__year=int(search))
        except (ValueError, TypeError):
            pass
        qs = qs.filter(
            pk_q |
            year_q |
            Q(planting__field__name__icontains=search) |
            Q(planting__variety__code__icontains=search) |
            Q(planting__variety__name__icontains=search) |
            Q(planting__season__icontains=search)
        )

    # Sorting
    sort = request.GET.get('sort', '-harvest_date')
    allowed_sorts = {
        '-harvest_date', 'harvest_date',
        '-yield_tons_per_ha', 'yield_tons_per_ha',
        'planting__field__name', '-planting__field__name',
        'planting__variety__code', '-planting__variety__code',
        'pk', '-pk',
    }
    if sort not in allowed_sorts:
        sort = '-harvest_date'
    qs = qs.order_by(sort)

    # Pagination
    _ALLOWED_PAGE_SIZES = {10, 25, 50, 100}
    try:
        page_size = int(request.GET.get('page_size', 25))
    except (ValueError, TypeError):
        page_size = 25
    if page_size not in _ALLOWED_PAGE_SIZES:
        page_size = 25

    page = request.GET.get('page', 1)
    paginator = Paginator(qs, page_size)
    try:
        page_obj = paginator.get_page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    query_string = _build_query_string(request)
    page_range = page_obj.paginator.get_elided_page_range(page_obj.number, on_each_side=1, on_ends=1)

    # Year options for filter dropdown
    years = sorted({d.year for d in HarvestRecord.objects.dates('harvest_date', 'year')}, reverse=True)

    # Field options for filter dropdown
    if role in ['admin', 'technician']:
        fields = Field.objects.filter(is_active=True).order_by('name')
    else:
        fields = Field.objects.filter(owner=user_profile, is_active=True).order_by('name')

    # Varieties list for filter dropdown
    varieties = [v[0] for v in services.get_variety_choices()]

    context = {
        'records': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'page_range': page_range,
        'query_string': query_string,
        'total_count': paginator.count,
        'search': search,
        'field_filter': field_filter,
        'variety_filter': variety_filter,
        'season_filter': season_filter,
        'year_filter': year_filter,
        'years': years,
        'fields': fields,
        'varieties': varieties,
        'sort_by': sort,
        'page_size': page_size,
    }
    return render(request, 'harvests/list.html', context)


@login_required(login_url=reverse_lazy('polls:login'))
def harvest_create(request):
    from .forms import HarvestRecordForm

    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')

    if request.method == 'POST':
        form = HarvestRecordForm(request.POST, user=request.user)
        if form.is_valid():
            record = form.save()
            messages.success(request, f"Harvest record for '{record.planting.field.name}' saved successfully.")
            return redirect('polls:harvests_list')
    else:
        form = HarvestRecordForm(user=request.user)

    return render(request, 'harvests/form.html', {
        'form': form,
        'is_edit': False,
    })


@login_required(login_url=reverse_lazy('polls:login'))
def harvest_edit(request, pk: int):
    from .forms import HarvestRecordForm

    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')

    # Role-based access control
    if user_profile.role in ['admin', 'technician']:
        record = get_object_or_404(HarvestRecord, pk=pk)
    else:
        record = get_object_or_404(HarvestRecord, pk=pk, planting__field__owner=user_profile)

    if request.method == 'POST':
        form = HarvestRecordForm(request.POST, instance=record, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Harvest record updated successfully.")
            return redirect('polls:harvests_list')
    else:
        form = HarvestRecordForm(instance=record, user=request.user)

    return render(request, 'harvests/form.html', {
        'form': form,
        'is_edit': True,
        'record': record,
    })


@login_required(login_url=reverse_lazy('polls:login'))
def harvest_archive(request, pk: int):
    """Soft-delete (archive) a harvest record."""
    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        messages.error(request, "Profile not found.")
        return redirect('polls:dashboard')

    if user_profile.role in ['admin', 'technician']:
        record = get_object_or_404(HarvestRecord, pk=pk)
    else:
        record = get_object_or_404(HarvestRecord, pk=pk, planting__field__owner=user_profile)

    if request.method == 'POST':
        record.delete()
        messages.success(request, "Harvest record archived successfully.")
        return redirect('polls:harvests_list')

    return redirect('polls:harvests_list')


@login_required(login_url=reverse_lazy('polls:login'))
@admin_only
def harvest_hard_delete(request, pk: int):
    """Hard delete a harvest record (admin only)."""
    record = get_object_or_404(HarvestRecord, pk=pk)
    if request.method == 'POST':
        if hasattr(record, 'purge'):
            record.purge()
        else:
            record.delete()
        messages.success(request, "Harvest record permanently deleted.")
        return redirect('polls:harvests_list')
    return redirect('polls:harvests_list')


# ============================================================================
# ADMIN USER MANAGEMENT VIEWS
# ============================================================================
from .decorators import admin_only

@login_required(login_url=reverse_lazy('polls:login'))
@admin_only
def admin_users_list(request):
    """List all users - Admin only with search, filter, and sort (BEST PRACTICE)."""
    from django.contrib.auth.models import User
    from django.db.models import Count, Q, Case, When, IntegerField
    
    # Search and filter parameters
    search_query = request.GET.get('q', '')
    role_filter = request.GET.get('role', '')
    status_filter = request.GET.get('status', '')  # active, inactive, pending
    sort_by = request.GET.get('sort', '-date_joined')  # Default: newest first
    
    users = User.objects.select_related('profile')
    
    # Apply search
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Apply role filter
    if role_filter:
        users = users.filter(profile__role=role_filter)
    
    # Apply status filter
    if status_filter == 'active':
        users = users.filter(is_active=True, profile__is_approved=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    elif status_filter == 'pending':
        users = users.filter(profile__is_approved=False)
    
    # Apply sorting (BEST PRACTICE: Multiple sort options)
    if sort_by == 'role' or sort_by == '-role':
        # Custom sort: admin → technician → farmer
        role_order = Case(
            When(profile__role='admin', then=1),
            When(profile__role='technician', then=2),
            When(profile__role='farmer', then=3),
            default=4,
            output_field=IntegerField()
        )
        if sort_by == 'role':
            users = users.annotate(role_order=role_order).order_by('role_order', 'username')
        else:  # -role (reverse)
            users = users.annotate(role_order=role_order).order_by('-role_order', 'username')
    elif sort_by == 'status' or sort_by == '-status':
        # Sort by status: active → pending → inactive
        status_order = Case(
            When(is_active=True, profile__is_approved=True, then=1),
            When(profile__is_approved=False, then=2),
            When(is_active=False, then=3),
            default=4,
            output_field=IntegerField()
        )
        if sort_by == 'status':
            users = users.annotate(status_order=status_order).order_by('status_order', 'username')
        else:
            users = users.annotate(status_order=status_order).order_by('-status_order', 'username')
    elif sort_by == 'name':
        users = users.order_by('first_name', 'last_name', 'username')
    elif sort_by == '-name':
        users = users.order_by('-first_name', '-last_name', '-username')
    elif sort_by == 'username':
        users = users.order_by('username')
    elif sort_by == '-username':
        users = users.order_by('-username')
    elif sort_by == 'date_joined':
        users = users.order_by('date_joined')  # Oldest first
    elif sort_by == '-date_joined':
        users = users.order_by('-date_joined')  # Newest first (default)
    elif sort_by == 'last_login':
        users = users.order_by('last_login')  # Oldest activity first
    elif sort_by == '-last_login':
        users = users.order_by('-last_login')  # Recent activity first
    else:
        users = users.order_by('-date_joined')  # Default fallback
    
    # Count users by role and status
    admin_count = User.objects.filter(profile__role='admin').count()
    technician_count = User.objects.filter(profile__role='technician').count()
    farmer_count = User.objects.filter(profile__role='farmer').count()
    pending_count = User.objects.filter(profile__is_approved=False).count()
    inactive_count = User.objects.filter(is_active=False).count()
    
    # Pagination
    allowed_page_sizes = [10, 20, 50, 100]
    try:
        page_size = int(request.GET.get('page_size', 20))
    except (TypeError, ValueError):
        page_size = 20
    if page_size not in allowed_page_sizes:
        page_size = 20

    paginator = Paginator(users, page_size)
    page = request.GET.get('page', 1)

    users_page = paginator.get_page(page)
    query_string = _build_query_string(request)

    context = {
        'users': users_page,
        'page_obj': users_page,
        'paginator': paginator,
        'is_paginated': users_page.has_other_pages(),
        'page_range': users_page.paginator.get_elided_page_range(users_page.number, on_each_side=1, on_ends=1),
        'total_users': User.objects.count(),
        'page_size': page_size,
        'allowed_page_sizes': allowed_page_sizes,
        'query_string': query_string,
        'admin_count': admin_count,
        'technician_count': technician_count,
        'farmer_count': farmer_count,
        'pending_count': pending_count,
        'inactive_count': inactive_count,
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'sort_by': sort_by,  # Pass current sort to template
    }
    return render(request, 'admin/users_list.html', context)



@login_required(login_url=reverse_lazy('polls:login'))
@admin_only
def admin_user_create(request):
    """Create technician or admin user - Admin only."""
    from .forms import AdminUserCreationForm
    
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User '{user.username}' created successfully with role: {user.profile.role}")
            return redirect('polls:admin_users_list')
    else:
        form = AdminUserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'admin/user_create.html', context)


@login_required(login_url=reverse_lazy('polls:login'))
@admin_only
def system_settings(request):
    """Web UI page para sa global system settings (Admin only).

    Tagalog:
    - Dito puwedeng itakda ng admin kung ilang araw pabalik ang pinapayagan
      na `planting_date` sa buong system.
    - Ginagamit ang `SiteSettingForm` para sa simple at safe na configuration.
    """
    setting = SiteSetting.objects.first()
    if not setting:
        # Gumawa ng default in-memory instance; mase-save lang kapag valid ang form.
        setting = SiteSetting()

    audits = []

    if request.method == "POST":
        # Capture the current values before binding form data, because ModelForm
        # may mutate the instance as it binds input values.
        prev_values = {
            "allowed_past_days_planting": setting.allowed_past_days_planting,
            "detection_confidence_threshold": setting.detection_confidence_threshold,
        }

        form = SiteSettingForm(request.POST, instance=setting)
        is_new = setting.pk is None

        if form.is_valid():
            setting = form.save()

            # Audit log (who/when/what changed).
            # Only record fields that actually changed to avoid confusing "30 → 30" entries.
            changes = {}
            for field, prev in prev_values.items():
                new = getattr(setting, field)
                if prev != new:
                    changes[field] = {"from": prev, "to": new}

            from .models import SiteSettingAudit

            audit_details = {
                "current": {
                    "allowed_past_days_planting": setting.allowed_past_days_planting,
                    "detection_confidence_threshold": setting.detection_confidence_threshold,
                },
                "changes": changes,
            }

            # If there were no actual changes, keep a trace so we still log the save action.
            if not changes:
                audit_details["note"] = "Saved without changes."

            SiteSettingAudit.objects.create(
                site_setting=setting,
                changed_by=request.user,
                details=audit_details,
            )

            messages.success(
                request,
                "System settings have been updated successfully.",
            )
            return redirect("polls:system_settings")
    else:
        form = SiteSettingForm(instance=setting)

    audits = list(setting.audits.filter(is_active=True).select_related("changed_by").all()[:10])

    current_allowed_days = services.get_allowed_past_days_for_planting()
    current_confidence_threshold = services.get_detection_confidence_threshold()

    recommended_defaults = getattr(settings, "SYSTEM_SETTING_DEFAULTS", {})

    context = {
        "form": form,
        "current_allowed_days": current_allowed_days,
        "current_confidence_threshold": current_confidence_threshold,
        "recommended_allowed_past_days": recommended_defaults.get("allowed_past_days_planting", 30),
        "recommended_confidence_threshold": recommended_defaults.get("detection_confidence_threshold", 75),
        "audits": audits,
    }
    return render(request, "admin/system_settings.html", context)


@login_required(login_url=reverse_lazy('polls:login'))
@admin_only
def system_settings_audit_list(request):
    """List all SiteSetting audit entries (admin only)."""
    from django.core.paginator import Paginator

    audits_qs = SiteSettingAudit.objects.select_related("changed_by")

    # Search + filters
    search = request.GET.get("search", "").strip()
    user_id = request.GET.get("user")
    field = request.GET.get("field")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")

    if search:
        audits_qs = audits_qs.filter(
            models.Q(changed_by__username__icontains=search)
            | models.Q(changed_by__first_name__icontains=search)
            | models.Q(changed_by__last_name__icontains=search)
            | models.Q(details__icontains=search)
        )

    if user_id:
        audits_qs = audits_qs.filter(changed_by__id=user_id)
    if field:
        audits_qs = audits_qs.filter(details__has_key=field)
    if date_from:
        try:
            from django.utils.dateparse import parse_date

            dt = parse_date(date_from)
            if dt:
                audits_qs = audits_qs.filter(changed_at__date__gte=dt)
        except Exception:
            pass
    if date_to:
        try:
            from django.utils.dateparse import parse_date

            dt = parse_date(date_to)
            if dt:
                audits_qs = audits_qs.filter(changed_at__date__lte=dt)
        except Exception:
            pass

    # Sorting
    sort = request.GET.get("sort", "newest")
    if sort == "oldest":
        audits_qs = audits_qs.order_by("changed_at")
    elif sort == "user":
        audits_qs = audits_qs.order_by("changed_by__username")
    elif sort == "-user":
        audits_qs = audits_qs.order_by("-changed_by__username")
    else:
        audits_qs = audits_qs.order_by("-changed_at")

    # Pagination
    try:
        page_size = int(request.GET.get("page_size", 25))
    except (TypeError, ValueError):
        page_size = 25

    page_size = max(1, min(page_size, 100))

    total_count = audits_qs.count()

    paginator = Paginator(audits_qs, page_size)
    page = request.GET.get("page", 1)
    audits = paginator.get_page(page)

    context = {
        "audits": audits,
        "total_count": total_count,
        "search_query": search,
        "sort": sort,
        "page_size": page_size,
        "filter_user": user_id or "",
        "filter_field": field or "",
        "filter_date_from": date_from or "",
        "filter_date_to": date_to or "",
        "filters_active": bool(search or user_id or field or date_from or date_to),
    }
    return render(request, "admin/system_settings_audit_list.html", context)


@login_required(login_url=reverse_lazy('polls:login'))
@admin_only
def system_settings_audit_revert(request, pk: int):
    """Revert SiteSetting values to the values stored in a specific audit entry."""
    audit = get_object_or_404(SiteSettingAudit, pk=pk)
    setting = audit.site_setting

    if request.method == "POST":
        details = audit.details or {}

        # `details` has evolved over time:
        # - Older entries may store {"field": value} or {"field": {"from":..., "to":...}}
        # - Newer entries store {"current": {...}, "changes": {...}}
        # Prefer the explicit `current` snapshot, then fall back to `changes`/values.
        if isinstance(details, dict) and isinstance(details.get("current"), dict):
            target_values = details["current"]
        elif isinstance(details, dict) and isinstance(details.get("changes"), dict):
            target_values = {f: diff.get("from") for f, diff in details["changes"].items() if isinstance(diff, dict)}
        elif isinstance(details, dict):
            target_values = details
        else:
            target_values = {}

        # Apply revert values and record what actually changed.
        changed = {}
        for field, new_value in target_values.items():
            if not hasattr(setting, field):
                continue

            old_value = getattr(setting, field)
            if old_value != new_value:
                setattr(setting, field, new_value)
                changed[field] = {"from": old_value, "to": new_value}

        if changed:
            setting.save()

            # Log the revert action
            SiteSettingAudit.objects.create(
                site_setting=setting,
                changed_by=request.user,
                details={
                    "reverted_from_audit": pk,
                    "changes": changed,
                },
            )

            messages.success(request, "System setting values have been reverted.")
        else:
            messages.info(request, "No revertable settings found in this audit entry.")

        return redirect("polls:system_settings_audit_list")

    # GET request: confirm
    return render(request, "admin/system_settings_audit_revert.html", {"audit": audit})


@login_required(login_url=reverse_lazy('polls:login'))
@admin_only
def system_settings_audit_bulk_archive(request):
    """Bulk-archive SiteSettingAudit entries via global Trash."""
    if request.method != 'POST':
        return redirect('polls:system_settings_audit_list')

    selected_ids = request.POST.getlist('selected_ids')
    if not selected_ids:
        messages.warning(request, "No audit entries were selected.")
        return redirect('polls:system_settings_audit_list')

    qs = SiteSettingAudit.objects.filter(pk__in=selected_ids, is_active=True)
    updated = qs.update(is_active=False)

    if updated:
        messages.success(request, f"{updated} audit entr{'y' if updated == 1 else 'ies'} archived. They can be restored from Trash & Archive.")
    else:
        messages.info(request, "No audit entries were archived.")

    return redirect('polls:system_settings_audit_list')


@login_required(login_url=reverse_lazy('polls:login'))
@admin_only
def system_settings_audit_archive(request, pk: int):
    """Archive a SiteSettingAudit entry (soft-delete) via global Trash."""
    audit = get_object_or_404(SiteSettingAudit, pk=pk)

    if request.method == 'POST':
        audit.is_active = False
        audit.save(update_fields=['is_active'])
        messages.success(request, "Audit entry archived. It can be restored from Trash & Archive.")
        return redirect('polls:system_settings_audit_list')

    return redirect('polls:system_settings_audit_list')


# -----------------------------------------------------------------------------
# Knowledge Base (Pests/Diseases/Nutrient Deficiencies)
# -----------------------------------------------------------------------------


@login_required(login_url=reverse_lazy('polls:login'))
def knowledge_list(request):
    """Farmer-facing knowledge base listing (published entries only)."""
    search = request.GET.get('search', '').strip()
    category = request.GET.get('category', '')
    sort = request.GET.get('sort', 'name')

    # Allow user to control page size (bounded to prevent abuse)
    try:
        page_size = int(request.GET.get('page_size', 12))
    except (ValueError, TypeError):
        page_size = 12
    page_size = max(5, min(page_size, 100))

    qs = KnowledgeBaseEntry.objects.filter(is_active=True, is_published=True)

    if search:
        qs = qs.filter(
            models.Q(name__icontains=search)
            | models.Q(description__icontains=search)
            | models.Q(symptoms__icontains=search)
            | models.Q(causes__icontains=search)
        )

    if category in (
        'disease', 'pest', 'crop_nutrition',
        'irrigation', 'soil', 'post_harvest'
    ):
        qs = qs.filter(category=category)

    # Sorting
    if sort == 'updated_at':
        qs = qs.order_by('-updated_at')
    elif sort == 'name':
        qs = qs.order_by('name')
    elif sort == '-name':
        qs = qs.order_by('-name')
    else:
        qs = qs.order_by('name')

    total_count = qs.count()
    paginator = Paginator(qs, page_size)
    page = request.GET.get('page', 1)
    entries = paginator.get_page(page)
    query_string = _build_query_string(request)
    page_range = entries.paginator.get_elided_page_range(entries.number, on_each_side=1, on_ends=1)

    is_admin_or_technician = False
    if hasattr(request.user, 'profile'):
        is_admin_or_technician = request.user.profile.role in ('admin', 'technician')

    context = {
        'entries': entries,
        'page_obj': entries,
        'is_paginated': entries.has_other_pages(),
        'page_range': page_range,
        'query_string': query_string,
        'search_query': search,
        'category_filter': category,
        'sort': sort,
        'page_size': page_size,
        'total_count': total_count,
        'is_admin_or_technician': is_admin_or_technician,
    }
    return render(request, 'knowledge/knowledge_list.html', context)


@login_required(login_url=reverse_lazy('polls:login'))
def knowledge_detail(request, pk: int):
    """Knowledge entry detail. Farmers only see published entries."""
    entry = get_object_or_404(KnowledgeBaseEntry, pk=pk, is_active=True)

    if not entry.is_published:
        # Only admin/tech can see unpublished entries
        if not request.user.is_authenticated or not hasattr(request.user, 'profile'):
            return redirect('polls:dashboard')
        if request.user.profile.role not in ('admin', 'technician'):
            return redirect('polls:dashboard')

    # Track view counts for knowledge trend analytics
    try:
        from django.db.models import F
        entry.view_count = F('view_count') + 1
        entry.save(update_fields=['view_count'])
        entry.refresh_from_db(fields=['view_count'])
    except Exception:
        pass

    return render(request, 'knowledge/knowledge_detail.html', {'entry': entry})


@login_required(login_url=reverse_lazy('polls:login'))
def knowledge_export_pdf(request, pk: int):
    """Export a knowledge entry as a PDF."""
    entry = get_object_or_404(KnowledgeBaseEntry, pk=pk, is_active=True)

    if not entry.is_published and (not hasattr(request.user, 'profile') or request.user.profile.role not in ('admin', 'technician')):
        return redirect('polls:dashboard')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    story = []
    story.append(Paragraph(entry.name, styles['Title']))
    story.append(Spacer(1, 12))

    # Include the image if available
    if getattr(entry, 'image', None):
        try:
            img_path = entry.image.path
            reader = ImageReader(img_path)
            iw, ih = reader.getSize()
            max_width = doc.width
            max_height = doc.height / 3
            scale = min(1, max_width / iw, max_height / ih)
            story.append(Image(img_path, width=iw * scale, height=ih * scale))
            story.append(Spacer(1, 12))
        except Exception:
            pass

    story.append(Paragraph(f"Category: {entry.get_category_display()}", styles['Normal']))
    story.append(Paragraph(f"Last updated: {entry.updated_at.strftime('%b %d, %Y')}", styles['Normal']))
    story.append(Spacer(1, 12))

    def add_section(title, text):
        story.append(Paragraph(f"<b>{title}</b>", styles['Heading3']))
        story.append(Paragraph(text.replace('\n', '<br/>'), styles['BodyText']))
        story.append(Spacer(1, 10))

    add_section('Overview', entry.description)
    add_section('Symptoms', entry.symptoms)
    add_section('Causes', entry.causes or 'N/A')
    add_section('Prevention', entry.prevention or 'N/A')

    doc.build(story)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="knowledge_{entry.pk}.pdf"'
    return response


@login_required(login_url=reverse_lazy('polls:login'))
def knowledge_export_csv(request, pk: int):
    """Export a knowledge entry as a simple CSV."""
    entry = get_object_or_404(KnowledgeBaseEntry, pk=pk, is_active=True)

    if not entry.is_published and (not hasattr(request.user, 'profile') or request.user.profile.role not in ('admin', 'technician')):
        return redirect('polls:dashboard')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="knowledge_{entry.pk}.csv"'
    writer = csv.writer(response)

    # Allow clients to pick which columns to include via ?cols=...
    cols = request.GET.getlist('cols')
    defaults = ['name', 'category', 'description', 'symptoms', 'causes', 'prevention', 'image_url', 'published', 'last_updated']
    if not cols:
        cols = defaults

    # Map keys to (label, value)
    values = {
        'name': ('Name', entry.name),
        'category': ('Category', entry.get_category_display()),
        'description': ('Description', entry.description),
        'symptoms': ('Symptoms', entry.symptoms),
        'causes': ('Causes', entry.causes or ''),
        'prevention': ('Prevention', entry.prevention or ''),
        'image_url': ('Image URL', request.build_absolute_uri(entry.image.url) if getattr(entry, 'image', None) else ''),
        'published': ('Published', 'Yes' if entry.is_published else 'No'),
        'last_updated': ('Last Updated', entry.updated_at.isoformat()),
    }

    writer.writerow(['Field', 'Value'])
    for c in cols:
        if c in values:
            label, val = values[c]
            writer.writerow([label, val])

    return response


@login_required(login_url=reverse_lazy('polls:login'))
@technician_or_admin
def knowledge_admin_list(request):
    """Admin/technician list view for managing knowledge base."""
    search = request.GET.get('search', '').strip()
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')

    qs = KnowledgeBaseEntry.objects.filter(is_active=True)

    if search:
        qs = qs.filter(
            models.Q(name__icontains=search)
            | models.Q(description__icontains=search)
            | models.Q(symptoms__icontains=search)
            | models.Q(causes__icontains=search)
        )

    if category in (
        'disease', 'pest', 'crop_nutrition',
        'irrigation', 'soil', 'post_harvest'
    ):
        qs = qs.filter(category=category)

    if status == 'published':
        qs = qs.filter(is_published=True)
    elif status == 'draft':
        qs = qs.filter(is_published=False)

    total_count = qs.count()

    allowed_page_sizes = [10, 20, 50, 100]
    try:
        page_size = int(request.GET.get('page_size', 20))
    except (ValueError, TypeError):
        page_size = 20
    if page_size not in allowed_page_sizes:
        page_size = 20

    paginator = Paginator(qs.order_by('-updated_at'), page_size)
    page = request.GET.get('page', 1)
    entries = paginator.get_page(page)

    query_string = _build_query_string(request)
    page_range = entries.paginator.get_elided_page_range(entries.number, on_each_side=1, on_ends=1)

    context = {
        'entries': entries,
        'page_obj': entries,
        'is_paginated': entries.has_other_pages(),
        'page_range': page_range,
        'query_string': query_string,
        'total_count': total_count,
        'search_query': search,
        'category_filter': category,
        'status_filter': status,
        'page_size': page_size,
        'allowed_page_sizes': allowed_page_sizes,
    }
    return render(request, 'knowledge/knowledge_admin_list.html', context)


@login_required(login_url=reverse_lazy('polls:login'))
@technician_or_admin
def knowledge_create(request):
    """Create a new knowledge base entry."""
    form = KnowledgeEntryForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        entry = form.save(commit=False)
        entry.created_by = request.user
        entry.save()
        messages.success(request, 'Knowledge entry created successfully.')
        return redirect('polls:knowledge_admin_list')

    return render(request, 'knowledge/knowledge_form.html', {'form': form, 'is_edit': False})


@login_required(login_url=reverse_lazy('polls:login'))
@technician_or_admin
def knowledge_edit(request, pk: int):
    """Edit an existing knowledge base entry."""
    entry = get_object_or_404(KnowledgeBaseEntry, pk=pk)
    form = KnowledgeEntryForm(request.POST or None, request.FILES or None, instance=entry)
    if request.method == 'POST' and form.is_valid():
        entry = form.save(commit=False)
        entry.save()
        messages.success(request, 'Knowledge entry saved successfully.')
        return redirect('polls:knowledge_admin_list')

    return render(request, 'knowledge/knowledge_form.html', {'form': form, 'entry': entry, 'is_edit': True})


@login_required(login_url=reverse_lazy('polls:login'))
@technician_or_admin
def knowledge_archive(request, pk: int):
    """Archive (soft-delete) a knowledge base entry via global Trash & Archive."""
    entry = get_object_or_404(KnowledgeBaseEntry, pk=pk, is_active=True)
    if request.method == 'POST':
        entry.is_active = False
        entry.is_published = False
        entry.save(update_fields=['is_active', 'is_published'])
        messages.success(request, 'Knowledge entry archived. It can be restored from Trash & Archive.')
    return redirect(f"{reverse('polls:trash_management')}?section=knowledge")


@login_required(login_url=reverse_lazy('polls:login'))
@admin_only
def admin_user_edit(request, pk: int):
    """Edit user account - Admin only."""
    from django.contrib.auth.models import User
    from .forms import AdminUserEditForm

    user = get_object_or_404(User, pk=pk)
    admin_count = User.objects.filter(profile__role='admin').count()
    is_last_admin = (hasattr(user, 'profile') and user.profile.role == 'admin' and admin_count <= 1)

    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, user=user)
        if form.is_valid():
            # Guard: prevent demoting the last admin
            new_role = form.cleaned_data.get('role')
            if is_last_admin and new_role != 'admin':
                messages.error(request, "Cannot change role — this is the only admin account. Promote another user to admin first.")
                context = {
                    'form': form,
                    'edit_user': user,
                    'admin_count': admin_count,
                    'is_last_admin': is_last_admin,
                }
                return render(request, 'admin/user_edit.html', context)

            form.save()

            if form.cleaned_data.get('reset_password'):
                messages.success(request, f"User '{user.username}' updated and password reset successfully!")
            else:
                messages.success(request, f"User '{user.username}' updated successfully!")

            return redirect('polls:admin_users_list')
    else:
        form = AdminUserEditForm(user=user)

    context = {
        'form': form,
        'edit_user': user,
        'admin_count': admin_count,
        'is_last_admin': is_last_admin,
    }
    return render(request, 'admin/user_edit.html', context)


@login_required(login_url=reverse_lazy('polls:login'))
@admin_only
def admin_user_toggle_active(request, pk: int):
    """Toggle user active status (activate/deactivate) - Admin only."""
    from django.contrib.auth.models import User
    
    user = get_object_or_404(User, pk=pk)
    
    # Prevent self-deactivation
    if user == request.user:
        messages.error(request, "You cannot deactivate your own account.")
        return redirect('polls:admin_users_list')
    
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f"User '{user.username}' has been {status}.")
        return redirect('polls:admin_users_list')
    
    context = {
        'user_to_toggle': user,
        'action': 'deactivate' if user.is_active else 'activate',
        'cancel_url': reverse('polls:admin_users_list'),
    }
    return render(request, 'admin/user_toggle_confirm.html', context)


@login_required(login_url=reverse_lazy('polls:login'))
@admin_only
def admin_user_approve(request, pk: int):
    """Approve pending farmer registration - Admin only."""
    from django.contrib.auth.models import User
    
    user = get_object_or_404(User, pk=pk)
    
    if not hasattr(user, 'profile'):
        messages.error(request, "User has no profile.")
        return redirect('polls:admin_users_list')
    
    # Approve user
    user.profile.is_approved = True
    user.profile.save()

    # Email the farmer: "Your account has been approved"
    try:
        from . import services as _svc
        # Tagalog: dynamic login URL para tugma sa dev/prod domain.
        login_url = _svc._app_url('/login/')
        _svc.send_plain_email(
            recipient_email=user.email,
            subject='[AgriScan+] Your Account Has Been Approved',
            body=(
                f"Hello {user.get_full_name() or user.username},\n\n"
                f"Great news! Your AgriScan+ farmer account has been approved by an administrator.\n"
                f"You can now log in and start using the system.\n\n"
                f"Log in here: {login_url}\n\n"
                f"---\nAgriScan+ System"
            ),
        )
    except Exception:
        pass  # Never block approval on email failure

    messages.success(request, f"User '{user.username}' has been approved and can now login.")
    return redirect('polls:admin_users_list')


@login_required(login_url=reverse_lazy('polls:login'))
@admin_only
def admin_user_delete(request, pk: int):
    """Delete a user - Admin only."""
    from django.contrib.auth.models import User
    
    user = get_object_or_404(User, pk=pk)
    
    # Prevent self-deletion
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('polls:admin_users_list')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' deleted successfully.")
        return redirect('polls:admin_users_list')
    return redirect('polls:admin_users_list')


# API Endpoints

@login_required(login_url=reverse_lazy('polls:login'))
def api_planting_data(request, pk):
    """
    API endpoint to get planting record data for auto-filling yield prediction form.
    Returns JSON with variety, area, planting_date, growth_duration_days.
    """
    from django.http import JsonResponse
    from .models import PlantingRecord
    
    try:
        planting = PlantingRecord.objects.select_related(
            'field', 'variety', 'field__owner'
        ).get(pk=pk)
        
        # Check access: farmers can only see their own plantings
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            if profile.role == 'farmer' and planting.field.owner != profile:
                return JsonResponse({'error': 'Permission denied'}, status=403)
        
        # Calculate growth duration
        if planting.expected_harvest_date:
            growth_days = (planting.expected_harvest_date - planting.planting_date).days
        elif planting.variety:
            growth_days = planting.variety.average_growth_days
        else:
            growth_days = 120
        
        hist = services.get_historical_yield_data(planting)
        data = {
            'variety': planting.variety.code if planting.variety else '',
            'area': float(planting.field.area_hectares),
            'planting_date': planting.planting_date.strftime('%Y-%m-%d'),
            'growth_duration_days': growth_days,
            'field_name': planting.field.name,
            'expected_harvest': planting.expected_harvest_date.strftime('%Y-%m-%d') if planting.expected_harvest_date else None,
            # Historical data from HarvestRecord history (2-year average)
            'historical_production_tons': float(hist.get('historical_production') or 0.0),
            'historical_yield_tons_per_ha': float(hist.get('historical_yield') or 0.0),
            'historical_source': hist.get('source'),
            'historical_record_count': int(hist.get('record_count', 0) or 0),
            # Include season/ecosystem for display in the front-end (read-only)
            'season': planting.season if planting and planting.season else None,
            'season_display': (planting.get_season_display() if planting and planting.season else planting.season) if planting else None,
            'ecosystem_type': planting.field.ecosystem_type if planting and planting.field else None,
            'ecosystem_type_display': (planting.field.get_ecosystem_type_display() if planting and planting.field and planting.field.ecosystem_type else planting.field.ecosystem_type) if planting and planting.field else None,
        }
        
        return JsonResponse(data)
        
    except PlantingRecord.DoesNotExist:
        return JsonResponse({'error': 'Planting record not found'}, status=404)


# ============================================================================
# TREATMENT MANAGEMENT VIEWS (Admin & Technician Only)
# ============================================================================

@login_required
@technician_or_admin
def treatments_list(request):
    """List all treatment recommendations with filtering, search, and sort."""
    from .models import TreatmentRecommendation
    
    # Get query parameters
    disease_filter = request.GET.get('disease', '')
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', 'all')
    sort_by = request.GET.get('sort', 'disease__name')
    
    # Base queryset
    treatments = TreatmentRecommendation.objects.select_related('disease')
    
    # Apply filters
    if disease_filter:
        treatments = treatments.filter(disease_id=disease_filter)
    
    if search_query:
        from django.db.models import Q
        pk_q = Q()
        try:
            pk_q = Q(pk=int(search_query))
        except (ValueError, TypeError):
            pass
        treatments = treatments.filter(
            pk_q |
            Q(disease__name__icontains=search_query) |
            Q(short_text__icontains=search_query) |
            Q(detailed_text__icontains=search_query) |
            Q(symptoms__icontains=search_query)
        )
    
    if status_filter == 'active':
        treatments = treatments.filter(is_active=True)
    elif status_filter == 'inactive':
        treatments = treatments.filter(is_active=False)

    # Sort functionality
    allowed_sorts = {
        'disease__name', '-disease__name',
        'priority', '-priority',
        'severity_min', '-severity_min',
        'pk', '-pk',
    }
    if sort_by not in allowed_sorts:
        sort_by = 'disease__name'
    treatments = treatments.order_by(sort_by)
    
    # Pagination
    allowed_page_sizes = [10, 20, 50, 100]
    try:
        page_size = int(request.GET.get('page_size', 20))
    except (TypeError, ValueError):
        page_size = 20
    if page_size not in allowed_page_sizes:
        page_size = 20

    paginator = Paginator(treatments, page_size)
    page = request.GET.get('page', 1)
    treatments_page = paginator.get_page(page)
    query_string = _build_query_string(request)

    # Get all diseases for filter dropdown
    from .models import DiseaseType
    diseases = DiseaseType.objects.all().order_by('name')
    
    context = {
        'treatments': treatments_page,
        'page_obj': treatments_page,
        'paginator': paginator,
        'is_paginated': treatments_page.has_other_pages(),
        'page_range': treatments_page.paginator.get_elided_page_range(treatments_page.number, on_each_side=1, on_ends=1),
        'query_string': query_string,
        'diseases': diseases,
        'disease_filter': disease_filter,
        'search_query': search_query,
        'status_filter': status_filter,
        'sort_by': sort_by,
        'total_count': treatments.count(),
        'page_size': page_size,
        'allowed_page_sizes': allowed_page_sizes,
    }
    
    return render(request, 'treatments/list.html', context)


@login_required
@technician_or_admin
def treatments_create(request):
    """Create a new treatment recommendation."""
    from .forms import TreatmentRecommendationForm
    
    if request.method == 'POST':
        form = TreatmentRecommendationForm(request.POST)
        if form.is_valid():
            treatment = form.save()
            messages.success(request, f'Treatment for "{treatment.disease.name}" created successfully!')
            return redirect('polls:treatments_list')
    else:
        form = TreatmentRecommendationForm()
    
    context = {
        'form': form,
        'title': 'Create Treatment Recommendation',
        'action': 'Create',
    }
    
    return render(request, 'treatments/form.html', context)


@login_required
@technician_or_admin
def treatments_edit(request, pk):
    """Edit an existing treatment recommendation."""
    from .models import TreatmentRecommendation
    from .forms import TreatmentRecommendationForm
    
    treatment = get_object_or_404(TreatmentRecommendation, pk=pk)
    
    if request.method == 'POST':
        form = TreatmentRecommendationForm(request.POST, instance=treatment)
        if form.is_valid():
            treatment = form.save()
            messages.success(request, f'Treatment for "{treatment.disease.name}" updated successfully!')
            return redirect('polls:treatments_list')
    else:
        form = TreatmentRecommendationForm(instance=treatment)
    
    context = {
        'form': form,
        'treatment': treatment,
        'title': f'Edit Treatment: {treatment.disease.name}',
        'action': 'Update',
    }
    
    return render(request, 'treatments/form.html', context)


@login_required
@admin_only
def treatments_delete(request, pk):
    """Archive a treatment recommendation (Admin only)."""
    from .models import TreatmentRecommendation
    
    treatment = get_object_or_404(TreatmentRecommendation, pk=pk)
    
    if request.method == 'POST':
        disease_name = treatment.disease.name
        treatment.is_active = False
        treatment.save(update_fields=['is_active'])
        messages.success(request, f'📦 Treatment for "{disease_name}" archived. Restore it anytime from Trash.')
        return redirect('polls:treatments_list')
    return redirect('polls:treatments_list')


# ============================================================================
# ANNOUNCEMENT SYSTEM VIEWS
# ============================================================================

@login_required
def announcements_list(request):
    """
    Display all announcements for the current user
    - Filters by role and targeting
    - Shows unread count
    - Paginated results
    - Handles mark_all_read POST action
    """
    from django.http import JsonResponse
    profile = request.user.profile

    # Handle mark_all_read POST action
    if request.method == 'POST' and request.POST.get('action') == 'mark_all_read':
        all_unread = services.get_user_announcements(profile, unread_only=True)
        from .models import Announcement
        for ann in all_unread:
            services.mark_announcement_as_read(ann, profile)
        messages.success(request, "All announcements marked as read.")
        return redirect('polls:announcements_list')

    # Check filter status first
    status_filter = request.GET.get('status')

    from .models import Announcement
    is_staff = profile.role in ('admin', 'technician')

    # Get announcements for this user with unread filter if needed
    if status_filter == 'unread':
        announcements = services.get_user_announcements(profile, unread_only=True)
    elif status_filter in ('active', 'draft') and is_staff:
        # Staff can filter by active/draft state (excludes deleted)
        all_ann = Announcement.objects.filter(is_deleted=False)
        announcements = all_ann.filter(is_active=(status_filter == 'active'))
    else:
        announcements = services.get_user_announcements(profile)

    # Filter by category if requested
    category = request.GET.get('category')
    if category:
        announcements = announcements.filter(category=category)

    # Filter by read status (for "read only" option)
    if status_filter == 'read':
        announcements = announcements.filter(is_read=True)

    # Search: title, content, or created_by username
    search = request.GET.get('search', '').strip()
    if search:
        from django.db.models import Q
        announcements = announcements.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(created_by__user__username__icontains=search) |
            Q(created_by__user__first_name__icontains=search) |
            Q(created_by__user__last_name__icontains=search)
        )

    # Pagination
    allowed_page_sizes = [10, 20, 50, 100]
    try:
        page_size = int(request.GET.get('page_size', 20))
    except (TypeError, ValueError):
        page_size = 20
    if page_size not in allowed_page_sizes:
        page_size = 20

    paginator = Paginator(announcements, page_size)
    page = request.GET.get('page', 1)
    announcements_page = paginator.get_page(page)
    query_string = _build_query_string(request)

    # Get unread count
    unread_count = services.get_unread_announcements_count(profile)

    # Draft / active counts (staff only, exclude deleted)
    if is_staff:
        draft_count = Announcement.objects.filter(is_active=False, is_deleted=False).count()
        active_count = Announcement.objects.filter(is_active=True, is_deleted=False).count()
    else:
        draft_count = 0
        active_count = 0

    # Get available categories for filter
    categories = Announcement.CATEGORY_CHOICES

    context = {
        'announcements': announcements_page,
        'page_obj': announcements_page,
        'paginator': paginator,
        'is_paginated': announcements_page.has_other_pages(),
        'page_range': announcements_page.paginator.get_elided_page_range(announcements_page.number, on_each_side=1, on_ends=1),
        'query_string': query_string,
        'unread_count': unread_count,
        'categories': categories,
        'current_category': category,
        'current_status': status_filter,
        'current_search': search,
        'draft_count': draft_count,
        'active_count': active_count,
        'is_staff': is_staff,
        'page_size': page_size,
        'allowed_page_sizes': allowed_page_sizes,
    }
    
    return render(request, 'announcements/list.html', context)


@login_required
def announcement_detail(request, pk):
    """
    Display full announcement and mark as read
    """
    from .models import Announcement
    
    profile = request.user.profile
    announcement = get_object_or_404(Announcement, pk=pk, is_active=True)
    
    # Check if user has access
    user_announcements = services.get_user_announcements(profile)
    if not user_announcements.filter(pk=pk).exists():
        messages.error(request, "You don't have permission to view this announcement.")
        return redirect('polls:announcements_list')
    
    # Mark as read
    services.mark_announcement_as_read(announcement, profile)
    
    # Get read status for this user
    from .models import UserNotification
    try:
        user_notif = UserNotification.objects.get(
            user=profile,
            announcement=announcement
        )
        is_read = user_notif.is_read
        read_at = user_notif.read_at
    except UserNotification.DoesNotExist:
        is_read = False
        read_at = None
    
    context = {
        'announcement': announcement,
        'is_read': is_read,
        'read_at': read_at,
    }
    
    return render(request, 'announcements/detail.html', context)


@login_required
def announcement_mark_read(request, pk):
    """
    AJAX endpoint to mark announcement as read
    """
    from django.http import JsonResponse
    from .models import Announcement
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)
    
    profile = request.user.profile
    announcement = get_object_or_404(Announcement, pk=pk, is_active=True)
    
    # Mark as read
    services.mark_announcement_as_read(announcement, profile)
    
    # Get new unread count
    unread_count = services.get_unread_announcements_count(profile)
    
    return JsonResponse({
        'success': True,
        'unread_count': unread_count,
    })


@login_required
@role_required(['admin', 'technician'])
def announcement_create(request):
    """
    Create new announcement (Admin/Technician only).
    If is_active=True: fires bell notifications + emails all targeted users.
    If is_active=False (draft): no notifications sent yet — fires on first activation.
    """
    from .forms import AnnouncementForm
    from .models import Announcement

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user.profile
            announcement.save()
            # signal notify_new_announcement fires automatically if is_active=True

            if announcement.is_active:
                # Also bulk-email (signal handles bell; we handle email here)
                try:
                    from . import services as _svc
                    sent = _svc.send_announcement_emails_to_targets(announcement) or 0
                except Exception:
                    sent = 0
                if sent:
                    messages.success(request, f'Announcement "{announcement.title}" published and emailed to {sent} user(s).')
                else:
                    messages.success(request, f'Announcement "{announcement.title}" published successfully!')
            else:
                messages.success(request, f'Announcement "{announcement.title}" saved as draft. Activate it later to notify users.')
            return redirect('polls:announcements_list')
    else:
        form = AnnouncementForm()

    context = {
        'form': form,
        'title': 'Create New Announcement',
        'submit_text': 'Save Announcement',
        'is_create': True,
        'is_admin': request.user.profile.role == 'admin',
    }

    return render(request, 'announcements/form.html', context)


@login_required
@role_required(['admin', 'technician'])
def announcement_edit(request, pk):
    """
    Edit existing announcement (Admin/Technician only).

    Draft → Active transition:
    - Fires bell notifications to all targeted users (same as create flow)
    - Re-sends bulk emails to targeted users

    published_at is locked (read-only) once the announcement has been activated.
    """
    from .forms import AnnouncementForm
    from .models import Announcement

    announcement = get_object_or_404(Announcement, pk=pk)
    was_active = announcement.is_active  # snapshot before POST

    # published_at is locked once the announcement has gone live (was_active=True and published_at set)
    publish_locked = was_active and announcement.published_at is not None

    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            updated = form.save(commit=False)
            # Backend protection: restore original published_at if locked
            if publish_locked:
                updated.published_at = announcement.published_at
            updated.save()

            # Draft → Active: send bell notifications + emails (only on first activation)
            if not was_active and updated.is_active:
                from .models import Notification, Profile
                from . import services as _svc
                from django.db.models import Q

                # Resolve target profiles
                audience = updated.target_audience
                if audience == 'all':
                    target_profiles = Profile.objects.filter(user__is_active=True).select_related('user')
                elif audience == 'farmers':
                    target_profiles = Profile.objects.filter(role='farmer', user__is_active=True).select_related('user')
                elif audience == 'technicians':
                    target_profiles = Profile.objects.filter(role='technician', user__is_active=True).select_related('user')
                elif audience == 'barangay' and updated.target_barangay:
                    target_profiles = Profile.objects.filter(
                        role='farmer', user__is_active=True,
                        fields__barangay__iexact=updated.target_barangay,
                    ).distinct().select_related('user')
                elif audience == 'user' and updated.target_user_id:
                    target_profiles = Profile.objects.filter(pk=updated.target_user_id).select_related('user')
                else:
                    target_profiles = Profile.objects.none()

                # Bell notifications (bulk_create, ignore duplicates)
                notifs = [
                    Notification(
                        recipient=profile,
                        type='advisory',
                        title=f'New Announcement: {updated.title}',
                        message=updated.content[:200] + ('...' if len(updated.content) > 200 else ''),
                        related_announcement=updated,
                    )
                    for profile in target_profiles
                ]
                created_notifs = []
                if notifs:
                    created_notifs = Notification.objects.bulk_create(notifs, ignore_conflicts=True)
                    for n in created_notifs:
                        _svc.send_notification_email(n)

                # Bulk email
                sent = _svc.send_announcement_emails_to_targets(updated) or 0
                target_count = target_profiles.count()
                messages.success(
                    request,
                    f'Announcement "{updated.title}" published! '
                    f'{target_count} user(s) notified via bell alert'
                    f'{f" and emailed to {sent}" if sent else ""}.'
                )
            else:
                messages.success(request, f'Announcement "{updated.title}" updated successfully!')
            return redirect('polls:announcements_list')
    else:
        form = AnnouncementForm(instance=announcement)

    context = {
        'form': form,
        'announcement': announcement,
        'title': 'Edit Announcement',
        'submit_text': 'Save Changes',
        'is_create': False,
        'is_admin': request.user.profile.role == 'admin',
        'publish_locked': publish_locked,
    }

    return render(request, 'announcements/form.html', context)


@login_required
@role_required(['admin'])
def announcement_delete(request, pk):
    """
    Archive announcement (Admin only)
    """
    from .models import Announcement
    
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        title = announcement.title
        announcement.is_deleted = True
        announcement.save(update_fields=['is_deleted'])
        messages.success(request, f'📦 Announcement "{title}" archived. Restore it anytime from Trash.')
        return redirect('polls:announcements_list')
    
    return redirect('polls:announcements_list')


# ============================================================================
# SYSTEM NOTIFICATIONS (Disease / Yield Drop / Announcement Alerts)
# Auto-generated by signals — not manually created by users.
# ============================================================================

@login_required
def notifications_list(request):
    """
    Display all system notifications for the current user.

    System notifications are auto-created when:
    - A disease is detected on a scan
    - A yield drop is predicted vs historical baseline
    - A new Announcement is published (bell alert)

    Supports:
    - Filter by type (disease / yield_drop / announcement)
    - Filter by read status (all / unread / read)
    - Mark all as read (POST)
    - Pagination (20 per page)
    """
    from .models import Notification

    profile = request.user.profile

    # Mark all as read (AJAX or form POST)
    if request.method == 'POST' and request.POST.get('action') == 'mark_all_read':
        Notification.objects.filter(recipient=profile, is_read=False).update(is_read=True)
        messages.success(request, 'All notifications marked as read.')
        return redirect('polls:notifications_list')

    notifications_qs = Notification.objects.filter(recipient=profile).select_related(
        'related_detection__disease',
        'related_yield__planting__field',
        'related_announcement',
    )

    # Filter by type
    type_filter = request.GET.get('type', '')
    if type_filter in ('disease', 'yield_drop', 'advisory'):
        notifications_qs = notifications_qs.filter(type=type_filter)

    # Filter by read status
    status_filter = request.GET.get('status', '')
    if status_filter == 'unread':
        notifications_qs = notifications_qs.filter(is_read=False)
    elif status_filter == 'read':
        notifications_qs = notifications_qs.filter(is_read=True)

    unread_count = Notification.objects.filter(recipient=profile, is_read=False).count()

    # Pagination
    allowed_page_sizes = [10, 20, 50, 100]
    try:
        page_size = int(request.GET.get('page_size', 20))
    except (TypeError, ValueError):
        page_size = 20
    if page_size not in allowed_page_sizes:
        page_size = 20

    paginator = Paginator(notifications_qs, page_size)
    page = request.GET.get('page', 1)
    notifications_page = paginator.get_page(page)
    query_string = _build_query_string(request)

    context = {
        'notifications': notifications_page,
        'page_obj': notifications_page,
        'paginator': paginator,
        'is_paginated': notifications_page.has_other_pages(),
        'page_range': notifications_page.paginator.get_elided_page_range(notifications_page.number, on_each_side=1, on_ends=1),
        'unread_count': unread_count,
        'type_filter': type_filter,
        'status_filter': status_filter,
        'total_count': paginator.count,
        'page_size': page_size,
        'allowed_page_sizes': allowed_page_sizes,
        'query_string': query_string,
    }
    return render(request, 'notifications/list.html', context)


@login_required
def notification_mark_read(request, pk):
    """
    AJAX endpoint to mark a single system notification as read.
    Returns JSON with updated unread_count.
    """
    from django.http import JsonResponse
    from .models import Notification

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

    profile = request.user.profile
    notification = get_object_or_404(Notification, pk=pk, recipient=profile)
    notification.is_read = True
    notification.save(update_fields=['is_read'])

    unread_count = Notification.objects.filter(recipient=profile, is_read=False).count()
    return JsonResponse({'success': True, 'unread_count': unread_count})


@login_required
def notification_mark_all_read(request):
    """
    AJAX/POST endpoint to mark ALL system notifications as read for current user.
    """
    from django.http import JsonResponse
    from .models import Notification

    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'}, status=405)

    profile = request.user.profile
    updated = Notification.objects.filter(recipient=profile, is_read=False).update(is_read=True)
    return JsonResponse({'success': True, 'marked': updated, 'unread_count': 0})


# ============================================================================
# RICE VARIETY MANAGEMENT (Best Practice - No Admin Panel)
# ============================================================================

@login_required
def varieties_list(request):
    """
    Display active rice varieties with search, sort, pagination, and bulk archive.
    Archived varieties are managed centrally via the Trash & Archive page.
    """
    profile = request.user.profile
    can_manage = profile.role in ['admin', 'technician']

    # ── Bulk archive (POST) ───────────────────────────────────────────────
    if request.method == 'POST' and can_manage:
        action = request.POST.get('bulk_action')
        pks    = request.POST.getlist('selected_ids')
        if action == 'archive' and pks:
            updated = RiceVariety.objects.filter(pk__in=pks, is_active=True).update(is_active=False)
            messages.success(request, f'📦 {updated} variet{"y" if updated == 1 else "ies"} archived.')
        return redirect(request.get_full_path())

    # Base queryset — active only, annotate planting count for sort + display
    qs = RiceVariety.objects.filter(is_active=True).annotate(
        planting_count=models.Count('plantings', filter=models.Q(plantings__is_active=True))
    )

    # ── Search — ID, code, name, developer, grain type ────────────────────
    search_query = request.GET.get('search', '').strip()
    if search_query:
        pk_q = models.Q()
        year_q = models.Q()
        try:
            num = int(search_query)
            pk_q   = models.Q(pk=num)
            year_q = models.Q(release_year=num)
        except (ValueError, TypeError):
            pass
        qs = qs.filter(
            pk_q | year_q |
            models.Q(code__icontains=search_query) |
            models.Q(name__icontains=search_query) |
            models.Q(developer__icontains=search_query) |
            models.Q(grain_type__icontains=search_query)
        )

    # ── Filters — variety_type, climate_type ──────────────────────────────
    filter_type    = request.GET.get('type', '').strip()
    filter_climate = request.GET.get('climate', '').strip()
    _VALID_TYPES    = {v for v, _ in RiceVariety.VarietyType.choices}
    _VALID_CLIMATES = {v for v, _ in RiceVariety.ClimateType.choices}
    if filter_type and filter_type in _VALID_TYPES:
        qs = qs.filter(variety_type=filter_type)
    else:
        filter_type = ''
    if filter_climate and filter_climate in _VALID_CLIMATES:
        qs = qs.filter(climate_type=filter_climate)
    else:
        filter_climate = ''

    # ── Sort ──────────────────────────────────────────────────────────────
    sort = request.GET.get('sort', 'code')
    _ALLOWED_SORTS = {
        'code', '-code',
        'name', '-name',
        'average_growth_days', '-average_growth_days',
        'average_yield_t_ha', '-average_yield_t_ha',
        'release_year', '-release_year',
        'pk', '-pk',
        'planting_count', '-planting_count',
    }
    if sort not in _ALLOWED_SORTS:
        sort = 'code'
    qs = qs.order_by(sort)

    # ── Page size ─────────────────────────────────────────────────────────
    _ALLOWED_PAGE_SIZES = {10, 25, 50, 100}
    try:
        page_size = int(request.GET.get('page_size', 25))
        if page_size not in _ALLOWED_PAGE_SIZES:
            page_size = 25
    except (ValueError, TypeError):
        page_size = 25

    # ── Pagination ────────────────────────────────────────────────────────
    paginator = Paginator(qs, page_size)
    page_num = request.GET.get('page')
    try:
        varieties_page = paginator.get_page(page_num)
    except (PageNotAnInteger, EmptyPage):
        varieties_page = paginator.get_page(1)

    query_string = _build_query_string(request)
    page_range = varieties_page.paginator.get_elided_page_range(varieties_page.number, on_each_side=1, on_ends=1)

    context = {
        'varieties': varieties_page,
        'page_obj': varieties_page,
        'is_paginated': varieties_page.has_other_pages(),
        'page_range': page_range,
        'query_string': query_string,
        'search_query': search_query,
        'sort': sort,
        'sort_by': sort,
        'total_count': paginator.count,
        'page_size': page_size,
        'can_manage': can_manage,
        # Filter state
        'filter_type': filter_type,
        'filter_climate': filter_climate,
        'variety_type_choices': RiceVariety.VarietyType.choices,
        'climate_type_choices': RiceVariety.ClimateType.choices,
        'filters_active': bool(search_query or filter_type or filter_climate),
        # Choice labels for display
        'resistance_labels': dict(RiceVariety.ResistanceLevel.choices),
    }

    return render(request, 'varieties/list.html', context)


@login_required
@role_required(['admin', 'technician'])
def variety_create(request):
    """
    Create a new rice variety.
    BEST PRACTICE: Custom form interface, restricted to admin/technician.
    """
    if request.method == 'POST':
        form = RiceVarietyForm(request.POST)
        if form.is_valid():
            variety = form.save()
            messages.success(
                request,
                f'✅ Rice variety "{variety.code}" created successfully!'
            )
            return redirect('polls:varieties_list')
    else:
        form = RiceVarietyForm()
    
    context = {
        'form': form,
        'title': 'Create Rice Variety',
        'submit_text': 'Create Variety',
        'cancel_url': reverse('polls:varieties_list'),
    }
    
    return render(request, 'varieties/form.html', context)


@login_required
@role_required(['admin', 'technician'])
def variety_edit(request, pk):
    """
    Edit an existing rice variety.
    BEST PRACTICE: Custom edit form with pre-filled data.
    """
    variety = get_object_or_404(RiceVariety, pk=pk)
    
    if request.method == 'POST':
        form = RiceVarietyForm(request.POST, instance=variety)
        if form.is_valid():
            variety = form.save()
            messages.success(
                request,
                f'✅ Rice variety "{variety.code}" updated successfully!'
            )
            return redirect('polls:varieties_list')
    else:
        form = RiceVarietyForm(instance=variety)
    
    context = {
        'form': form,
        'variety': variety,
        'title': f'Edit Rice Variety: {variety.code}',
        'submit_text': 'Save Changes',
        'cancel_url': reverse('polls:varieties_list'),
    }
    
    return render(request, 'varieties/form.html', context)


@login_required
@role_required(['admin', 'technician'])
def variety_delete(request, pk):
    """
    Archive (soft-delete) a rice variety.
    Permanent delete is handled exclusively from the Trash & Archive page.
    """
    variety = get_object_or_404(RiceVariety, pk=pk)

    if request.method == 'POST':
        variety.delete()
        messages.success(
            request,
            f'📦 Variety "{variety.code}" archived. '
            f'Existing plantings are preserved. You can restore it anytime from Trash.'
        )
        return redirect('polls:varieties_list')
    return redirect('polls:varieties_list')


@login_required
@role_required(['admin', 'technician'])
def variety_restore(request, pk):
    """Restore a soft-deleted (archived) rice variety back to active."""
    variety = get_object_or_404(RiceVariety, pk=pk)

    if request.method == 'POST':
        variety.is_active = True
        variety.save(update_fields=['is_active'])
        messages.success(
            request,
            f'✅ Variety "{variety.code}" restored and is now active again.'
        )
    return redirect('polls:varieties_list')


# ============================================================================
# TRASH / ARCHIVE MANAGEMENT
# Central soft-delete management for admin & technician.
# ============================================================================

@login_required
@role_required(['admin', 'technician'])
def trash_management(request):
    """
    Central Trash & Archive page.
    - GET: supports ?section=<model>&search=<q>&sort=<field>&order=asc|desc
    - POST: action=restore|purge, model=<name>, pk=<id>
    """
    from django.db.models.deletion import ProtectedError
    from .models import Field, PlantingRecord, DetectionRecord, YieldPrediction, HarvestRecord, RiceVariety, Announcement, SiteSettingAudit, KnowledgeBaseEntry, TreatmentRecommendation

    # ── POST: restore or purge ────────────────────────────────────────────────
    if request.method == 'POST':
        action     = request.POST.get('action')
        model_name = request.POST.get('model')
        obj_pk     = request.POST.get('pk')

        # Announcement uses is_deleted flag (not is_active) — handle separately
        if model_name == 'announcement':
            try:
                obj = Announcement.objects.get(pk=obj_pk, is_deleted=True)
                if action == 'restore':
                    obj.is_deleted = False
                    obj.save(update_fields=['is_deleted'])
                    messages.success(request, f'✅ Announcement #{obj_pk} restored successfully.')
                elif action == 'purge':
                    obj.delete()
                    messages.warning(request, f'🗑️ Announcement #{obj_pk} permanently deleted.')
            except Announcement.DoesNotExist:
                messages.error(request, 'Announcement not found or not in trash.')
        else:
            model_map  = {
                'field': Field, 'planting': PlantingRecord, 'detection': DetectionRecord,
                'yield': YieldPrediction, 'harvest': HarvestRecord, 'variety': RiceVariety,
                'season_log': SeasonLog, 'audit': SiteSettingAudit,
                'knowledge': KnowledgeBaseEntry, 'treatment': TreatmentRecommendation,
            }
            model_cls = model_map.get(model_name)
            if model_cls and obj_pk:
                try:
                    obj = model_cls.all_objects.get(pk=obj_pk, is_active=False)
                    if action == 'restore':
                        obj.is_active = True
                        obj.save(update_fields=['is_active'])
                        messages.success(request, f'✅ {model_name.capitalize()} #{obj_pk} restored successfully.')
                    elif action == 'purge':
                        try:
                            if hasattr(obj, 'purge'):
                                obj.purge()
                            elif hasattr(obj, 'hard_delete'):
                                obj.hard_delete()
                            else:
                                obj.delete()
                            messages.warning(request, f'🗑️ {model_name.capitalize()} #{obj_pk} permanently deleted.')
                        except ProtectedError:
                            messages.error(request, f'Error: {model_name.capitalize()} #{obj_pk} cannot be deleted due to protected related records.')
                except model_cls.DoesNotExist:
                    messages.error(request, 'Record not found or already active.')
        # Preserve section/search/sort/order on redirect
        qs_str = request.POST.get('_qs', '')
        return redirect(f"{reverse('polls:trash_management')}{'?' + qs_str if qs_str else ''}")

    # ── GET params ────────────────────────────────────────────────────────────
    section = request.GET.get('section', 'all')   # all | variety | field | planting | detection | yield | season_log | announcement
    search  = request.GET.get('search', '').strip()
    sort    = request.GET.get('sort', 'newest')    # newest | oldest | name | id
    order   = request.GET.get('order', 'desc')     # asc | desc  (for name/id)

    VALID_SECTIONS = {'all', 'variety', 'field', 'planting', 'detection', 'yield', 'harvest', 'season_log', 'announcement', 'audit', 'knowledge', 'treatment'}
    VALID_SORTS    = {'newest', 'oldest', 'name', 'id'}
    if section not in VALID_SECTIONS: section = 'all'
    if sort    not in VALID_SORTS:    sort    = 'newest'
    if order   not in {'asc', 'desc'}: order  = 'desc'

    def _sort_qs(qs, name_field='name'):
        if sort == 'newest':
            return qs.order_by('-updated_at') if hasattr(qs.model, 'updated_at') else qs.order_by('-pk')
        if sort == 'oldest':
            return qs.order_by('updated_at') if hasattr(qs.model, 'updated_at') else qs.order_by('pk')
        if sort == 'name':
            return qs.order_by(name_field if order == 'asc' else f'-{name_field}')
        if sort == 'id':
            return qs.order_by('pk' if order == 'asc' else '-pk')
        return qs

    # ── Build querysets ───────────────────────────────────────────────────────
    varieties_qs      = RiceVariety.all_objects.filter(is_active=False)
    fields_qs         = Field.all_objects.filter(is_active=False).select_related('owner__user')
    plantings_qs      = PlantingRecord.all_objects.filter(is_active=False).select_related('field', 'variety')
    detections_qs     = DetectionRecord.all_objects.filter(is_active=False).select_related('disease', 'planting__field', 'user__user')
    yields_qs         = YieldPrediction.all_objects.filter(is_active=False).select_related('planting__field', 'planting__variety')
    harvests_qs       = HarvestRecord.all_objects.filter(is_active=False).select_related('planting__field', 'planting__variety')
    season_logs_qs    = SeasonLog.all_objects.filter(is_active=False).select_related('farmer__user', 'field', 'variety')
    announcements_qs  = Announcement.objects.filter(is_deleted=True).select_related('created_by__user')
    audit_qs          = SiteSettingAudit.all_objects.filter(is_active=False).select_related('changed_by')
    knowledge_qs      = KnowledgeBaseEntry.all_objects.filter(is_active=False).select_related('created_by')
    treatments_qs     = TreatmentRecommendation.all_objects.filter(is_active=False).select_related('disease')

    # ── Apply search ──────────────────────────────────────────────────────────
    if search:
        # Varieties: code or name (already good)
        varieties_qs  = varieties_qs.filter(models.Q(code__icontains=search) | models.Q(name__icontains=search))

        # Fields: name, barangay, owner username/first/last
        fields_qs     = fields_qs.filter(
            models.Q(name__icontains=search)
            | models.Q(barangay__icontains=search)
            | models.Q(owner__user__username__icontains=search)
            | models.Q(owner__user__first_name__icontains=search)
            | models.Q(owner__user__last_name__icontains=search)
        )

        # Plantings: field name, field barangay, variety code/name, notes
        plantings_qs  = plantings_qs.filter(
            models.Q(field__name__icontains=search)
            | models.Q(field__barangay__icontains=search)
            | models.Q(variety__code__icontains=search)
            | models.Q(variety__name__icontains=search)
            | models.Q(notes__icontains=search)
        )

        # Detections: disease, field name, variety code/name, reporting user, treatment text
        detections_qs = detections_qs.filter(
            models.Q(disease__name__icontains=search)
            | models.Q(planting__field__name__icontains=search)
            | models.Q(planting__variety__code__icontains=search)
            | models.Q(planting__variety__name__icontains=search)
            | models.Q(user__user__username__icontains=search)
            | models.Q(treatment_text__icontains=search)
        )

        # Yields: field name, field barangay, variety code/name, model_version
        yields_qs     = yields_qs.filter(
            models.Q(planting__field__name__icontains=search)
            | models.Q(planting__field__barangay__icontains=search)
            | models.Q(planting__variety__code__icontains=search)
            | models.Q(planting__variety__name__icontains=search)
            | models.Q(model_version__icontains=search)
        )

        # Season Logs: field name, variety, farmer name, season year
        season_logs_qs = season_logs_qs.filter(
            models.Q(field__name__icontains=search)
            | models.Q(field__barangay__icontains=search)
            | models.Q(variety__code__icontains=search)
            | models.Q(variety__name__icontains=search)
            | models.Q(farmer__user__username__icontains=search)
            | models.Q(farmer__user__first_name__icontains=search)
            | models.Q(farmer__user__last_name__icontains=search)
            | models.Q(season_year__icontains=search)
        )

        # Announcements: title, content, created_by username
        announcements_qs = announcements_qs.filter(
            models.Q(title__icontains=search)
            | models.Q(content__icontains=search)
            | models.Q(created_by__user__username__icontains=search)
            | models.Q(created_by__user__first_name__icontains=search)
            | models.Q(created_by__user__last_name__icontains=search)
        )

        # System settings audit: user, or any text in details JSON
        audit_qs = audit_qs.filter(
            models.Q(changed_by__username__icontains=search)
            | models.Q(changed_by__first_name__icontains=search)
            | models.Q(changed_by__last_name__icontains=search)
            | models.Q(details__icontains=search)
        )

        # Knowledge base: name, description, symptoms, causes, author
        knowledge_qs = knowledge_qs.filter(
            models.Q(name__icontains=search)
            | models.Q(description__icontains=search)
            | models.Q(symptoms__icontains=search)
            | models.Q(causes__icontains=search)
            | models.Q(created_by__username__icontains=search)
            | models.Q(created_by__first_name__icontains=search)
            | models.Q(created_by__last_name__icontains=search)
        )

        # Treatments: disease name, short/detailed text
        treatments_qs = treatments_qs.filter(
            models.Q(disease__name__icontains=search)
            | models.Q(short_text__icontains=search)
            | models.Q(detailed_text__icontains=search)
        )

    # ── Apply sort ────────────────────────────────────────────────────────────
    varieties_qs      = _sort_qs(varieties_qs,      'code')
    fields_qs         = _sort_qs(fields_qs,         'name')
    plantings_qs      = _sort_qs(plantings_qs,      'field__name')
    detections_qs     = _sort_qs(detections_qs,     'disease__name')
    yields_qs         = _sort_qs(yields_qs,         'planting__field__name')
    season_logs_qs    = _sort_qs(season_logs_qs,    'field__name')
    announcements_qs  = _sort_qs(announcements_qs,  'title')
    audit_qs          = _sort_qs(audit_qs,          'changed_at')
    knowledge_qs      = _sort_qs(knowledge_qs,      'name')
    treatments_qs     = _sort_qs(treatments_qs,     'disease__name')

    # ── Section filter ────────────────────────────────────────────────────────
    trash = {
        'varieties':      varieties_qs      if section in ('all', 'variety')      else RiceVariety.objects.none(),
        'fields':         fields_qs         if section in ('all', 'field')         else Field.objects.none(),
        'plantings':      plantings_qs      if section in ('all', 'planting')      else PlantingRecord.objects.none(),
        'detections':     detections_qs     if section in ('all', 'detection')     else DetectionRecord.objects.none(),
        'yields':         yields_qs         if section in ('all', 'yield')         else YieldPrediction.objects.none(),
        'harvests':       harvests_qs       if section in ('all', 'harvest')       else HarvestRecord.objects.none(),
        'season_logs':    season_logs_qs    if section in ('all', 'season_log')    else SeasonLog.objects.none(),
        'announcements':  announcements_qs  if section in ('all', 'announcement')  else Announcement.objects.none(),
        'audits':         audit_qs         if section in ('all', 'audit')        else SiteSettingAudit.objects.none(),
        'knowledge':      knowledge_qs      if section in ('all', 'knowledge')     else KnowledgeBaseEntry.objects.none(),
        'treatments':     treatments_qs     if section in ('all', 'treatment')     else TreatmentRecommendation.objects.none(),
    }

    # Raw counts per section (unfiltered, for sidebar badges)
    counts = {
        'variety':      RiceVariety.all_objects.filter(is_active=False).count(),
        'field':        Field.all_objects.filter(is_active=False).count(),
        'planting':     PlantingRecord.all_objects.filter(is_active=False).count(),
        'detection':    DetectionRecord.all_objects.filter(is_active=False).count(),
        'yield':        YieldPrediction.all_objects.filter(is_active=False).count(),
        'harvest':      HarvestRecord.all_objects.filter(is_active=False).count(),
        'season_log':   SeasonLog.all_objects.filter(is_active=False).count(),
        'announcement': Announcement.objects.filter(is_deleted=True).count(),
        'audit':        SiteSettingAudit.all_objects.filter(is_active=False).count(),
        'knowledge':    KnowledgeBaseEntry.all_objects.filter(is_active=False).count(),
        'treatment':    TreatmentRecommendation.all_objects.filter(is_active=False).count(),
    }
    total_archived  = sum(counts.values())
    total_displayed = sum(qs.count() for qs in trash.values())

    context = {
        'trash': trash,
        'counts': counts,
        'total_archived': total_archived,
        'total_displayed': total_displayed,
        'is_admin': request.user.profile.role == 'admin',
        # filter state
        'section': section,
        'search': search,
        'sort': sort,
        'order': order,
        # querystring for POST redirect preservation
        '_qs': request.GET.urlencode(),
    }
    return render(request, 'trash/management.html', context)


# ============================================================================
# SEASON FARM LOG — Farmer Activity Journal / History
# ============================================================================

@login_required(login_url=reverse_lazy('polls:login'))
def season_log_list(request):
    """List all season logs.
    - Farmers see only their own logs.
    - Admin/Technician see all with barangay/variety stats.
    """
    from django.db.models import Count, Sum, Avg, Q

    profile = request.user.profile
    role    = profile.role

    qs = SeasonLog.objects.filter(is_active=True).select_related(
        'farmer__user', 'field', 'variety'
    )

    if role == 'farmer':
        qs = qs.filter(farmer=profile)

    # ── Filters ──────────────────────────────────────────────────────────
    search     = request.GET.get('search', '').strip()
    year_f     = request.GET.get('year', '')
    season_f   = request.GET.get('season', '')
    stage_f    = request.GET.get('stage', '')
    variety_f  = request.GET.get('variety', '')

    if search:
        qs = qs.filter(
            Q(field__name__icontains=search) |
            Q(variety__name__icontains=search) |
            Q(variety__code__icontains=search) |
            Q(farmer__user__first_name__icontains=search) |
            Q(farmer__user__last_name__icontains=search) |
            Q(field__barangay__icontains=search) |
            Q(summary_notes__icontains=search)
        )
    if year_f:
        qs = qs.filter(season_year=year_f)
    if season_f:
        qs = qs.filter(season_type=season_f)
    if stage_f:
        qs = qs.filter(current_stage=stage_f)
    if variety_f:
        qs = qs.filter(variety__pk=variety_f)

    # ── Stats (for header cards) ─────────────────────────────────────────
    total_count    = qs.count()
    harvested_qs   = qs.filter(current_stage='harvested', actual_yield_sacks__isnull=False)
    avg_yield      = harvested_qs.aggregate(avg=Avg('actual_yield_sacks'))['avg']
    total_income   = harvested_qs.aggregate(s=Sum('gross_income'))['s']

    # Variety adoption: how many farmers used each variety this year
    current_year   = timezone.now().year
    variety_stats  = (
        SeasonLog.objects.filter(is_active=True, season_year=current_year)
        .exclude(variety__isnull=True)
        .values('variety__name', 'variety__code', 'field__barangay')
        .annotate(farmer_count=Count('farmer', distinct=True))
        .order_by('-farmer_count')[:10]
    )

    # ── Pagination ───────────────────────────────────────────────────────
    allowed_page_sizes = [10, 20, 50, 100]
    try:
        page_size = int(request.GET.get('page_size', 20))
    except (TypeError, ValueError):
        page_size = 20
    if page_size not in allowed_page_sizes:
        page_size = 20

    paginator = Paginator(qs, page_size)
    page = request.GET.get('page', 1)
    logs = paginator.get_page(page)
    query_string = _build_query_string(request)

    # ── Filter option lists ──────────────────────────────────────────────
    years    = SeasonLog.objects.filter(is_active=True).values_list(
        'season_year', flat=True).distinct().order_by('-season_year')
    varieties = RiceVariety.objects.filter(is_active=True).order_by('name')

    return render(request, 'season_log/list.html', {
        'logs':          logs,
        'page_obj':      logs,
        'paginator':     paginator,
        'is_paginated':  logs.has_other_pages(),
        'page_range':    logs.paginator.get_elided_page_range(logs.number, on_each_side=1, on_ends=1),
        'total_count':   total_count,
        'avg_yield':     round(avg_yield, 1) if avg_yield else None,
        'total_income':  total_income,
        'variety_stats': variety_stats,
        'role':          role,
        'page_size':     page_size,
        'allowed_page_sizes': allowed_page_sizes,
        'query_string': query_string,
        # filters
        'search':     search,
        'year_f':     year_f,
        'season_f':   season_f,
        'stage_f':    stage_f,
        'variety_f':  variety_f,
        'years':      years,
        'varieties':  varieties,
        'season_choices': SeasonLog.SEASON_CHOICES,
        'stage_choices':  SeasonLog.STAGE_CHOICES,
    })


@login_required(login_url=reverse_lazy('polls:login'))
def season_log_detail(request, pk):
    """Full timeline of a single season — all activities in chronological order."""
    from django.db.models import Sum

    profile = request.user.profile
    log     = get_object_or_404(SeasonLog, pk=pk, is_active=True)

    # Permission: farmer can only see own logs
    if profile.role == 'farmer' and log.farmer != profile:
        messages.error(request, "You don't have permission to view this log.")
        return redirect('polls:season_log_list')

    activities = log.activities.select_related(
        'detection_record__disease'
    ).order_by('activity_date', 'created_at')

    # Cost summary
    cost_summary = activities.aggregate(
        total_input  = Sum('input_cost'),
        total_labor  = Sum('labor_cost'),
    )
    total_cost = (
        float(cost_summary['total_input']  or 0) +
        float(cost_summary['total_labor']  or 0)
    )

    # Problems summary
    problems = activities.exclude(problem_severity='none').exclude(problem_observed='')

    # Activity type breakdown
    from django.db.models import Count
    activity_breakdown = activities.values('activity_type').annotate(
        cnt=Count('id')
    ).order_by('-cnt')

    # Barangay-level variety adoption
    if log.variety:
        same_variety_count = SeasonLog.objects.filter(
            is_active=True,
            variety=log.variety,
            season_year=log.season_year,
            field__barangay=log.field.barangay,
        ).count()
    else:
        same_variety_count = None

    return render(request, 'season_log/detail.html', {
        'log':               log,
        'activities':        activities,
        'problems':          problems,
        'cost_summary':      cost_summary,
        'total_cost':        total_cost,
        'activity_breakdown': activity_breakdown,
        'same_variety_count': same_variety_count,
        'role':              profile.role,
    })


def _build_plantings_json(farmer):
    """Return a JSON-serializable dict of PlantingRecord data keyed by pk,
    used by the season log create form to auto-fill fields on planting selection."""
    import json
    if not farmer:
        return json.dumps({})
    qs = PlantingRecord.objects.filter(
        field__owner=farmer, is_active=True, season_log__isnull=True
    ).select_related('field', 'variety').order_by('-planting_date')
    data = {}
    for p in qs:
        data[str(p.pk)] = {
            'field_id':      p.field_id,
            'variety_id':    p.variety_id,
            'date_planted':  p.planting_date.isoformat() if p.planting_date else '',
            'date_harvested': p.expected_harvest_date.isoformat() if p.expected_harvest_date else '',
        }
    return json.dumps(data)


@login_required(login_url=reverse_lazy('polls:login'))
def season_log_create(request):
    """Create a new season log."""
    from django.db import IntegrityError
    profile  = request.user.profile
    is_staff = profile.role in ('admin', 'technician')

    # Admin/tech: can log for ANY active user/profile
    if is_staff:
        from .models import Field as FieldModel
        profiles_with_fields = Profile.objects.filter(
            user__is_active=True
        ).select_related('user').order_by(
            'role', 'user__last_name', 'user__first_name'
        )
        profile_id = request.POST.get('profile_id') or request.GET.get('profile_id')
        try:
            target_profile = Profile.objects.get(pk=profile_id) if profile_id else None
        except Profile.DoesNotExist:
            target_profile = None
        # Check if the selected profile actually has fields
        target_has_fields = (
            FieldModel.objects.filter(owner=target_profile, is_active=True).exists()
            if target_profile else False
        )
    else:
        profiles_with_fields = None
        target_profile       = profile
        target_has_fields    = True

    if request.method == 'POST':
        # If admin changed the profile dropdown, reload with new profile's fields
        if is_staff and request.POST.get('change_owner') == '1':
            from django.utils import timezone as tz
            form = SeasonLogForm(owner_profile=target_profile, initial={'season_year': tz.now().year})
            return render(request, 'season_log/form.html', {
                'form': form, 'form_title': 'New Season Log',
                'subtitle': 'Start a new crop season journal', 'is_create': True,
                'role': profile.role, 'is_staff': is_staff,
                'profiles': profiles_with_fields, 'target_profile': target_profile,
                'target_has_fields': target_has_fields,
                'plantings_json': _build_plantings_json(target_profile),
            })
        form = SeasonLogForm(request.POST, owner_profile=target_profile)
        if form.is_valid():
            log        = form.save(commit=False)
            log.farmer = target_profile if target_profile else profile
            # Link the chosen PlantingRecord (non-model field — apply manually)
            chosen_planting = form.cleaned_data.get('planting')
            if chosen_planting:
                log.planting = chosen_planting
            try:
                log.save()
                _push_recent_activity(request, f"Created season log: {log.season_label} @ {log.field}")
                messages.success(request, f"Season log created: {log.season_label} @ {log.field.name}")
                return redirect('polls:season_log_detail', pk=log.pk)
            except IntegrityError:
                form.add_error(None, "A season log for this field, year, and season type already exists.")
    else:
        from django.utils import timezone as tz
        form = SeasonLogForm(
            owner_profile=target_profile,
            initial={'season_year': tz.now().year}
        )

    return render(request, 'season_log/form.html', {
        'form':              form,
        'form_title':        'New Season Log',
        'subtitle':          'Start a new crop season journal',
        'is_create':         True,
        'role':              profile.role,
        'is_staff':          is_staff,
        'profiles':          profiles_with_fields,
        'target_profile':    target_profile,
        'target_has_fields': target_has_fields,
        'plantings_json':    _build_plantings_json(target_profile),
    })


@login_required(login_url=reverse_lazy('polls:login'))
def season_log_edit(request, pk):
    """Edit an existing season log."""
    from django.db import IntegrityError
    profile  = request.user.profile
    log      = get_object_or_404(SeasonLog, pk=pk, is_active=True)
    is_staff = profile.role in ('admin', 'technician')

    if profile.role == 'farmer' and log.farmer != profile:
        messages.error(request, "You don't have permission to edit this log.")
        return redirect('polls:season_log_list')

    # For admin/tech: the log already has a farmer; pass their profile
    target_profile = log.farmer

    if request.method == 'POST':
        form = SeasonLogForm(request.POST, instance=log, owner_profile=target_profile)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Season log updated.")
                return redirect('polls:season_log_detail', pk=log.pk)
            except IntegrityError:
                form.add_error(None, "A season log for this field, year, and season type already exists.")
    else:
        form = SeasonLogForm(instance=log, owner_profile=target_profile)

    return render(request, 'season_log/form.html', {
        'form':          form,
        'log':           log,
        'form_title':    f'Edit: {log.season_label}',
        'subtitle':      f'{log.field.name}',
        'is_create':     False,
        'role':          profile.role,
        'is_staff':      is_staff,
        'target_profile': target_profile,
    })


@login_required(login_url=reverse_lazy('polls:login'))
def season_log_delete(request, pk):
    """Soft-delete a season log."""
    profile = request.user.profile
    log     = get_object_or_404(SeasonLog, pk=pk, is_active=True)

    if profile.role == 'farmer' and log.farmer != profile:
        messages.error(request, "You don't have permission to delete this log.")
        return redirect('polls:season_log_list')

    if request.method == 'POST':
        log.is_active = False
        log.save(update_fields=['is_active'])
        messages.success(request, f"Season log '{log.season_label}' deleted.")
        return redirect('polls:season_log_list')
    return redirect('polls:season_log_list')


@login_required(login_url=reverse_lazy('polls:login'))
def activity_create(request, season_pk):
    """Add a farm activity to a season log."""
    profile    = request.user.profile
    season_log = get_object_or_404(SeasonLog, pk=season_pk, is_active=True)

    if profile.role == 'farmer' and season_log.farmer != profile:
        messages.error(request, "You don't have permission.")
        return redirect('polls:season_log_list')

    if request.method == 'POST':
        form = FarmActivityForm(request.POST, season_log=season_log, owner_profile=profile)
        if form.is_valid():
            activity            = form.save(commit=False)
            activity.season_log = season_log
            activity.save()

            # ── Auto-advance season stage based on activity type ──────────
            stage_map = {
                'land_prep':    'land_prep',
                'seedbed':      'land_prep',
                'transplanting':'planting',
                'fertilizer':   'growing',
                'pesticide':    'growing',
                'fungicide':    'growing',
                'herbicide':    'growing',
                'foliar':       'growing',
                'irrigation':   'growing',
                'scouting':     'growing',
                'disease_obs':  'growing',
                'harvest':      'harvested',
            }
            STAGE_ORDER = ['planning', 'land_prep', 'planting', 'growing', 'harvest_ready', 'harvested']
            desired_stage = stage_map.get(activity.activity_type)
            if desired_stage:
                current_idx = STAGE_ORDER.index(season_log.current_stage) if season_log.current_stage in STAGE_ORDER else 0
                desired_idx = STAGE_ORDER.index(desired_stage)
                update_fields = []
                if desired_idx > current_idx:
                    season_log.current_stage = desired_stage
                    update_fields.append('current_stage')
                if activity.activity_type == 'harvest':
                    if activity.activity_date and not season_log.date_harvested:
                        season_log.date_harvested = activity.activity_date
                        update_fields.append('date_harvested')
                if update_fields:
                    season_log.save(update_fields=update_fields)

            _push_recent_activity(request, f"Logged activity: {activity.title[:40]}")
            messages.success(request, f"Activity logged: {activity.get_activity_type_display()}")
            return redirect('polls:season_log_detail', pk=season_pk)
    else:
        form = FarmActivityForm(
            season_log=season_log,
            owner_profile=profile,
            initial={'activity_date': timezone.now().date()}
        )

    return render(request, 'season_log/activity_form.html', {
        'form':       form,
        'season_log': season_log,
        'form_title': 'Log Farm Activity',
        'is_create':  True,
        'role':       profile.role,
    })


@login_required(login_url=reverse_lazy('polls:login'))
def activity_edit(request, pk):
    """Edit a farm activity log entry."""
    profile  = request.user.profile
    activity = get_object_or_404(FarmActivity, pk=pk)
    log      = activity.season_log

    if profile.role == 'farmer' and log.farmer != profile:
        messages.error(request, "You don't have permission.")
        return redirect('polls:season_log_list')

    if request.method == 'POST':
        form = FarmActivityForm(request.POST, instance=activity,
                                season_log=log, owner_profile=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Activity updated.")
            return redirect('polls:season_log_detail', pk=log.pk)
    else:
        form = FarmActivityForm(instance=activity, season_log=log, owner_profile=profile)

    return render(request, 'season_log/activity_form.html', {
        'form':       form,
        'season_log': log,
        'activity':   activity,
        'form_title': 'Edit Activity',
        'is_create':  False,
        'role':       profile.role,
    })


@login_required(login_url=reverse_lazy('polls:login'))
def activity_delete(request, pk):
    """Delete a farm activity entry."""
    profile  = request.user.profile
    activity = get_object_or_404(FarmActivity, pk=pk)
    log      = activity.season_log

    if profile.role == 'farmer' and log.farmer != profile:
        messages.error(request, "You don't have permission.")
        return redirect('polls:season_log_list')

    if request.method == 'POST':
        log_pk = log.pk
        activity.delete()
        messages.success(request, "Activity entry deleted.")
        return redirect('polls:season_log_detail', pk=log_pk)
    return redirect('polls:season_log_detail', pk=log.pk)


@login_required(login_url=reverse_lazy('polls:login'))
def season_log_barangay_stats(request):
    """DA/Admin view: variety adoption + yield stats grouped by barangay."""
    from django.db.models import Count, Sum, Avg

    profile = request.user.profile
    if profile.role == 'farmer':
        messages.error(request, "Access restricted to DA officers and technicians.")
        return redirect('polls:season_log_list')

    year_f   = request.GET.get('year', str(timezone.now().year))
    season_f = request.GET.get('season', '')

    qs = SeasonLog.objects.filter(is_active=True)
    if year_f:
        qs = qs.filter(season_year=year_f)
    if season_f:
        qs = qs.filter(season_type=season_f)

    # Barangay × Variety adoption
    barangay_stats = (
        qs.exclude(variety__isnull=True)
        .values('field__barangay', 'variety__name', 'variety__code')
        .annotate(
            farmer_count   = Count('farmer', distinct=True),
            total_area_ha  = Sum('field__area_hectares'),
            avg_yield_sacks = Avg('actual_yield_sacks'),
            total_yield     = Sum('actual_yield_sacks'),
        )
        .order_by('field__barangay', '-farmer_count')
    )

    # Top varieties overall
    top_varieties = (
        qs.exclude(variety__isnull=True)
        .values('variety__name', 'variety__code')
        .annotate(farmer_count=Count('farmer', distinct=True))
        .order_by('-farmer_count')[:8]
    )

    years    = SeasonLog.objects.values_list(
        'season_year', flat=True).distinct().order_by('-season_year')

    return render(request, 'season_log/barangay_stats.html', {
        'barangay_stats': barangay_stats,
        'top_varieties':  top_varieties,
        'years':          years,
        'year_f':         year_f,
        'season_f':       season_f,
        'season_choices': SeasonLog.SEASON_CHOICES,
        'role':           profile.role,
    })
