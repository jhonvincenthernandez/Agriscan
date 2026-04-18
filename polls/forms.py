from __future__ import annotations

from django import forms
from django.conf import settings

from .models import (
    DetectionRecord,
    YieldPrediction,
    HarvestRecord,
    TreatmentRecommendation,
    DiseaseType,
    RiceVariety,
    SeasonLog,
    FarmActivity,
    Field,
    PlantingRecord,
    KnowledgeBaseEntry,
)
from django import forms as django_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile
User = get_user_model()

def get_health_choices(user=None):
    """
    Get health choices from actual detection records.
    BEST PRACTICE:
    - Role-based filtering: farmers see only their own detections.
    - Exclude 'Unknown/Not Rice' detections — they carry no valid disease/health
      data and would only confuse the yield model.
    """
    from .services import UNKNOWN_LABEL
    try:
        from .models import DetectionRecord

        qs = DetectionRecord.objects.select_related(
            'disease', 'planting', 'planting__field'
        ).exclude(
            # Exclude unclassified / non-rice detections at DB level
            disease__name=UNKNOWN_LABEL
        ).order_by('-created_at')

        # ── Role-based filtering ──────────────────────────────────────────────
        if user is not None and hasattr(user, 'profile'):
            profile = user.profile
            if profile.role == 'farmer':
                # Farmers see only detections they submitted
                qs = qs.filter(user=profile)
            # admin / technician → no extra filter (see all)

        qs = qs[:50]  # Cap at 50 for performance

        choices = [("", "-- Select Health Status --")]

        for det in qs:
            date_str = det.created_at.strftime('%Y-%m-%d')
            field_name = det.planting.field.name if det.planting and det.planting.field else "Unknown"

            if det.disease and det.severity_pct is not None:
                label = f"🦠 {det.disease.name} ({det.severity_pct}%) - {date_str} - {field_name} [ID:{det.pk}]"
            else:
                label = f"✅ Healthy - {date_str} - {field_name} [ID:{det.pk}]"

            choices.append((str(det.pk), label))

        if len(choices) > 1:
            return choices
    except Exception:
        pass

    # Fallback if no detections found
    return [
        ("", "-- Select Health Status --"),
        ("0", "✅ Healthy (No disease detected)"),
        ("0.5", "⚠️ Moderate disease presence"),
        ("1.0", "🔴 Severe disease detected"),
    ]

DEFAULT_VARIETIES = (
    ("Rc222", "Rc222"),
    ("Rc160", "Rc160"),
    ("Rc216", "Rc216"),
)

YIELD_MODEL_CHOICES = (
    ("linear_regression", "Linear Regression (Tabular Data)"),
    ("cnn_yield", "CNN Yield (Canopy Image)"),
)

INPUT_CLASS = "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"


class LeafScanForm(forms.Form):
    """
    Simple image upload form for disease detection.
    BEST PRACTICE: Role-based planting queryset with searchable dropdown.
    """

    leaf_image = forms.ImageField(
        label="Upload or Capture Image",
        required=True,
        widget=forms.ClearableFileInput(
            attrs={
                "accept": "image/*",
                "capture": "environment",
                "class": "mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500",
            }
        ),
    )
    
    planting = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=True,
        label="Planting Cycle",
        help_text="Search and select the planting cycle for this detection",
        widget=forms.Select(attrs={
            "class": "mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500",
            "data-searchable": "true",  # Enable searchable dropdown
        })
    )
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import PlantingRecord
        
        if user and hasattr(user, 'profile'):
            user_profile = user.profile
            role = user_profile.role
            
            # BEST PRACTICE: Role-based access control
            if role in ['admin', 'technician']:
                # Admin/Technician can see ALL active planting cycles
                queryset = PlantingRecord.objects.filter(is_active=True)
            else:
                # Farmers see only their own active planting cycles
                queryset = PlantingRecord.objects.filter(field__owner=user_profile, is_active=True)
            
            self.fields['planting'].queryset = queryset.select_related(
                'field', 
                'field__owner', 
                'field__owner__user',
                'variety'
            ).order_by('-planting_date')
            
            # Custom label — guard against variety=None (nullable FK)
            self.fields['planting'].label_from_instance = lambda obj: (
                f"{obj.field.name} - {obj.variety.code if obj.variety else 'No variety'} "
                f"(Planted: {obj.planting_date.strftime('%b %d, %Y')}) "
                f"[Owner: {obj.field.owner.user.get_full_name() or obj.field.owner.user.username}]"
                if role in ['admin', 'technician'] else
                f"{obj.field.name} - {obj.variety.code if obj.variety else 'No variety'} (Planted: {obj.planting_date.strftime('%b %d, %Y')})"
            )
        else:
            # Fallback: show active-only (shouldn't happen with @login_required)
            self.fields['planting'].queryset = PlantingRecord.objects.filter(
                is_active=True
            ).select_related(
                'field', 'variety'
            ).order_by('-planting_date')
    
    def clean(self):
        """Validate that planting is selected"""
        cleaned_data = super().clean()
        planting = cleaned_data.get('planting')
        
        if not planting:
            raise forms.ValidationError(
                "Please select a planting cycle. This is required to track which field and crop the detection belongs to."
            )
        
        return cleaned_data


class YieldPredictionForm(forms.Form):
    """
    Collect agronomic features needed by the yield model.
    
    BEST PRACTICE: Allow selecting PlantingRecord to auto-fill all data
    from actual planting cycle (variety, field, dates, historical data, etc.)
    
    New structure based on industry-standard parameters:
    - Core inputs (REQUIRED): area, historical data, planting date, growth duration, variety
    - Optional inputs (enhance accuracy): season, health status, environmental data
    """

    selected_model = forms.ChoiceField(
        choices=YIELD_MODEL_CHOICES,
        required=True,
        initial="linear_regression",
        label="Yield Model",
        widget=forms.Select(attrs={"class": INPUT_CLASS, "id": "id_selected_model"}),
        help_text="Pumili ng model: Linear Regression para tabular data o CNN para canopy image.",
    )

    canopy_image = forms.ImageField(
        required=False,
        label="Canopy Image (Required for CNN mode)",
        widget=forms.ClearableFileInput(
            attrs={
                "accept": "image/*",
                "capture": "environment",
                "class": "mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500",
            }
        ),
        help_text="Top-down canopy photo near harvest (~0.8-0.9m distance).",
    )
    
    # Option 1: Select existing planting record (BEST PRACTICE - auto-fills everything)
    planting = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        label="Select Planting Record (Recommended - Auto-fills all fields)",
        widget=forms.Select(attrs={
            "class": INPUT_CLASS,
            "id": "id_planting",
            "data-searchable": "true",
        }),
        help_text="Search and select the planting cycle to auto-fill all required data"
    )
    
    # Option 2: Manual entry (REQUIRED if no planting record selected)
    # Core inputs
    area = forms.DecimalField(
        min_value=0.01,
        max_digits=7,
        decimal_places=2,
        label="Field Area (hectares) *",
        widget=forms.NumberInput(attrs={"step": "0.01", "class": INPUT_CLASS}),
        required=False,
        help_text="Size of the planted field"
    )

    historical_production_tons = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        required=False,
        label="Historical Production (tons)",
        widget=forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
        help_text="Total production from recent harvests (used to compute yield per hectare).",
    )

    historical_yield_tons_per_ha = forms.DecimalField(
        min_value=0,
        max_digits=8,
        decimal_places=2,
        required=False,
        label="Historical Yield (tons/ha)",
        widget=forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
        help_text="Yield per hectare (auto-calculated from production and area).",
    )
    
    variety = forms.ChoiceField(
        choices=DEFAULT_VARIETIES, 
        widget=forms.Select(attrs={"class": INPUT_CLASS}),
        required=False,
        label="Rice Variety *",
        help_text="Rice variety affects yield potential"
    )
    
    planting_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": INPUT_CLASS}),
        required=False,
        label="Planting Date *",
        help_text="Date when the field was planted"
    )
    
    average_growth_duration_days = forms.IntegerField(
        min_value=40,
        max_value=200,
        label="Average Growth Duration (days) *",
        widget=forms.NumberInput(attrs={"class": INPUT_CLASS, "min": "40", "max": "200"}),
        required=False,
        help_text="Number of days until harvest (typically 90-150 days)"
    )

    # NOTE: Ang mga field na ito ay display-only. Kinukuha mula sa PlantingRecord/Field
    # para makita ng user ang season at ecosystem type nang hindi na ito nae-edit.
    season = forms.CharField(
        required=False,
        label="Season",
        widget=forms.TextInput(attrs={
            "class": INPUT_CLASS + " bg-gray-50 cursor-not-allowed",
            "readonly": "readonly",
            "disabled": "disabled",
            "id": "id_season_display",
        }),
        help_text="Read-only display of season from the selected planting record.",
    )

    ecosystem_type = forms.CharField(
        required=False,
        label="Ecosystem Type",
        widget=forms.TextInput(attrs={
            "class": INPUT_CLASS + " bg-gray-50 cursor-not-allowed",
            "readonly": "readonly",
            "disabled": "disabled",
            "id": "id_ecosystem_type_display",
        }),
        help_text="Read-only display of ecosystem type from the selected field.",
    )
    
    # Optional inputs (enhance accuracy)
    health = forms.ChoiceField(
        widget=forms.Select(attrs={
            "class": INPUT_CLASS,
            "id": "id_health_select",
            "data-search": "true",
        }), 
        label="Health Status (Optional - from disease detection)",
        required=False,
        help_text="Select from recent disease detections to improve accuracy"
    )

    def __init__(self, *args, variety_choices=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        from . import services

        # Tagalog: Kapag disabled ang CNN sa system settings, LR lang ang puwedeng piliin.
        if not services.get_yield_cnn_enabled():
            self.fields['selected_model'].choices = (
                ('linear_regression', 'Linear Regression (Tabular Data)'),
            )
            self.fields['selected_model'].initial = 'linear_regression'
        
        # Set variety choices
        if variety_choices:
            self.fields["variety"].choices = variety_choices
        # Pass user so farmers only see their own detections in the health dropdown
        self.fields["health"].choices = get_health_choices(user=user)
        
        # Set planting queryset based on user (BEST PRACTICE - role-based)
        if user:
            from .models import PlantingRecord
            if hasattr(user, 'profile'):
                profile = user.profile
                if profile.role == 'admin' or profile.role == 'technician':
                    # Admin/tech see all plantings
                    self.fields['planting'].queryset = PlantingRecord.objects.select_related(
                        'field', 'variety', 'field__owner'
                    ).order_by('-planting_date')
                else:
                    # Farmers see only their plantings
                    self.fields['planting'].queryset = PlantingRecord.objects.filter(
                        field__owner=profile
                    ).select_related('field', 'variety').order_by('-planting_date')
            else:
                self.fields['planting'].queryset = PlantingRecord.objects.none()
        else:
            from .models import PlantingRecord
            self.fields['planting'].queryset = PlantingRecord.objects.all().select_related(
                'field', 'variety'
            ).order_by('-planting_date')
    
    def clean(self):
        cleaned_data = super().clean()
        planting = cleaned_data.get('planting')
        selected_model = cleaned_data.get('selected_model') or 'linear_regression'

        from . import services

        # Tagalog: Huwag payagan ang CNN mode kapag naka-disable sa settings.
        if selected_model == 'cnn_yield' and not services.get_yield_cnn_enabled():
            self.add_error('selected_model', 'CNN yield mode is currently disabled by system settings.')

        # Tagalog: Sa CNN mode, canopy image ang pangunahing required input.
        if selected_model == 'cnn_yield' and not cleaned_data.get('canopy_image'):
            self.add_error('canopy_image', 'Canopy image is required when CNN yield model is selected.')
        
        # If planting selected, no need for manual fields
        if planting:
            return cleaned_data
        
        # Tagalog: Model-specific required fields para hindi naghahalo ang assumptions.
        if selected_model == 'cnn_yield':
            required_fields = ['area', 'planting_date', 'average_growth_duration_days']
        else:
            required_fields = ['area', 'variety', 'planting_date', 'average_growth_duration_days']

        missing = [f for f in required_fields if not cleaned_data.get(f)]
        
        if missing:
            raise forms.ValidationError(
                f"Either select a Planting Record or provide all core fields. "
                f"Missing required fields: {', '.join(missing)}"
            )
        
        return cleaned_data


class DetectionRecordForm(forms.ModelForm):
    """Administer detection records, with optional image replacement."""

    new_image = forms.ImageField(
        label="Replace image",
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "accept": "image/*",
                "class": "mt-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500",
            }
        ),
    )

    class Meta:
        model = DetectionRecord
        fields = [
            "disease",
            "confidence_pct",
            "severity_pct",
            "model_version",
            "source",
        ]
        labels = {
            "disease": "Disease",
            "confidence_pct": "Confidence (%)",
            "severity_pct": "Severity (%)",
            "model_version": "Model Version",
            "source": "Source",
        }
        help_texts = {
            "source": "Where this detection originated. Defaults to Web.",
        }
        widgets = {
            "disease": forms.Select(attrs={"class": INPUT_CLASS}),
            "confidence_pct": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0", "max": "100"}),
            "severity_pct": forms.NumberInput(attrs={"class": INPUT_CLASS, "min": "0", "max": "100"}),
            "model_version": forms.Select(attrs={"class": INPUT_CLASS}),
            "source": forms.Select(attrs={"class": INPUT_CLASS}, choices=[("web", "Web"), ("mobile", "Mobile"), ("api", "API")]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["source"].widget = forms.Select(attrs={"class": INPUT_CLASS}, choices=[("web", "Web"), ("mobile", "Mobile"), ("api", "API")])
        if not self.instance.pk:
            self.fields["source"].initial = "web"

    def clean_confidence_pct(self):
        value = self.cleaned_data.get("confidence_pct")
        if value is not None and (value < 0 or value > 100):
            raise forms.ValidationError("Confidence must be between 0 and 100.")
        return value

    def clean_severity_pct(self):
        value = self.cleaned_data.get("severity_pct")
        if value is not None and (value < 0 or value > 100):
            raise forms.ValidationError("Severity must be between 0 and 100.")
        return value


class YieldPredictionRecordForm(forms.ModelForm):
    """Manage stored yield prediction records."""

    class Meta:
        model = YieldPrediction
        fields = [
            "planting",
            "detection",
            "predicted_sacks_per_ha",
            "confidence_pct",
            "area_hectares",
            "total_sacks",
            "total_tons",
            "harvest_date",
            "model_meta",
        ]
        labels = {
            "planting": "Planting Record",
            "detection": "Detection Record",
            "predicted_sacks_per_ha": "Predicted Sacks per Hectare",
            "confidence_pct": "Confidence (%)",
            "area_hectares": "Area (hectares)",
            "total_sacks": "Total Sacks",
            "total_tons": "Total Tons",
            "harvest_date": "Harvest Date",
            "model_meta": "Model Metadata",
        }
        widgets = {
            "planting": forms.Select(attrs={"class": INPUT_CLASS}),
            "detection": forms.Select(attrs={"class": INPUT_CLASS}),
            "predicted_sacks_per_ha": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01"}),
            "confidence_pct": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0", "max": "100"}),
            "area_hectares": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0"}),
            "total_sacks": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0"}),
            "total_tons": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0"}),
            "harvest_date": forms.DateInput(attrs={"type": "date", "class": INPUT_CLASS}),
            "model_meta": forms.Textarea(attrs={"class": INPUT_CLASS + " resize-y", "rows": 3}),
        }

    def clean_confidence_pct(self):
        value = self.cleaned_data.get("confidence_pct")
        if value is not None and (value < 0 or value > 100):
            raise forms.ValidationError("Confidence must be between 0 and 100.")
        return value

    def clean(self):
        data = super().clean()
        for key in ("predicted_sacks_per_ha", "area_hectares", "total_sacks", "total_tons"):
            value = data.get(key)
            if value is not None and value < 0:
                self.add_error(key, "Value cannot be negative.")
        return data


class HarvestRecordForm(forms.ModelForm):
    """Create and edit actual harvest records.

    Yield (tons/ha) is auto-calculated from harvested weight and area.
    """

    yield_tons_per_ha = forms.DecimalField(
        min_value=0,
        max_digits=8,
        decimal_places=2,
        required=False,
        label="Yield (tons/ha)",
        widget=forms.NumberInput(attrs={"class": INPUT_CLASS, "readonly": "readonly"}),
    )

    class Meta:
        model = HarvestRecord
        fields = [
            "planting",
            "harvest_date",
            "actual_yield_tons",
            "area_harvested_ha",
            "grain_quality",
            "notes",
        ]
        labels = {
            "planting": "Planting Record",
            "harvest_date": "Harvest Date",
            "actual_yield_tons": "Actual Yield (tons)",
            "area_harvested_ha": "Area Harvested (ha)",
            "yield_tons_per_ha": "Yield (tons/ha)",
            "grain_quality": "Grain Quality",
            "notes": "Notes",
        }
        widgets = {
            "planting": forms.Select(attrs={"class": INPUT_CLASS, "data-searchable": "true"}),
            "harvest_date": forms.DateInput(attrs={"type": "date", "class": INPUT_CLASS}),
            "actual_yield_tons": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0"}),
            "area_harvested_ha": forms.NumberInput(attrs={"class": INPUT_CLASS, "step": "0.01", "min": "0"}),
            "grain_quality": forms.Select(attrs={"class": INPUT_CLASS}),
            "notes": forms.Textarea(attrs={"class": INPUT_CLASS + " resize-y", "rows": 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Role-based queryset for planting selection
        if user and hasattr(user, 'profile'):
            profile = user.profile
            if profile.role in ['admin', 'technician']:
                qs = PlantingRecord.objects.filter(status__in=['planned', 'ongoing'], is_active=True)
            else:
                qs = PlantingRecord.objects.filter(
                    field__owner=profile,
                    status__in=['planned', 'ongoing'],
                    is_active=True,
                )
        else:
            qs = PlantingRecord.objects.filter(status__in=['planned', 'ongoing'], is_active=True)

        # Ensure editing an existing record doesn't fail validation if the planted cycle
        # is no longer in the current selectable queryset (e.g., status changed).
        instance_planting_id = getattr(getattr(self, 'instance', None), 'planting_id', None)
        if instance_planting_id:
            qs = PlantingRecord.objects.filter(pk=instance_planting_id) | qs

        self.fields['planting'].queryset = qs.select_related('field', 'variety').order_by('-planting_date')

        # Display rich label for planting selector
        self.fields['planting'].label_from_instance = lambda obj: (
            f"{obj.field.name} — {obj.variety.code if obj.variety else 'No variety'} "
            f"({obj.season.capitalize()}, Cycle {obj.cropping_cycle or '?'})"
        )

    def clean(self):
        cleaned = super().clean()
        planting = cleaned.get('planting')

        # Allow editing an existing harvest record even if the planting already has one.
        # The `planting.harvest_record_id` is only validated when it's a different record.
        if planting:
            existing_harvest_id = getattr(planting, 'harvest_record_id', None)
            if existing_harvest_id and existing_harvest_id != getattr(self.instance, 'pk', None):
                raise forms.ValidationError(
                    "A harvest record already exists for the selected planting cycle. "
                    "Update the existing record instead."
                )
        return cleaned


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": INPUT_CLASS}))
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": INPUT_CLASS}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": INPUT_CLASS})
        self.fields["password2"].widget.attrs.update({"class": INPUT_CLASS})
    
    def clean_email(self):
        """
        BEST PRACTICE: Validate email uniqueness during registration.
        Prevents duplicate emails and provides clear error message.
        """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered. Please use a different email or login.")
        return email


class ProfileForm(django_forms.Form):
    """
    Edit a user's profile (user fields + Profile fields).
    
    BEST PRACTICE: farm_size_ha is auto-computed from fields, so it's read-only here.
    """

    first_name = django_forms.CharField(required=False, label="First name", widget=django_forms.TextInput(attrs={"class": INPUT_CLASS}))
    last_name = django_forms.CharField(required=False, label="Last name", widget=django_forms.TextInput(attrs={"class": INPUT_CLASS}))
    email = django_forms.EmailField(required=True, label="Email", widget=django_forms.EmailInput(attrs={"class": INPUT_CLASS}))
    phone = django_forms.CharField(required=False, label="Phone", widget=django_forms.TextInput(attrs={"class": INPUT_CLASS}))
    location = django_forms.CharField(required=False, label="Location", widget=django_forms.TextInput(attrs={"class": INPUT_CLASS}))
    # farm_size_ha removed - it's auto-computed from Field model
    notes = django_forms.CharField(required=False, label="Notes", widget=django_forms.Textarea(attrs={"class": INPUT_CLASS + " resize-none", "rows": 3}))

    def __init__(self, *args, user: User = None, profile: Profile = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user  # keep reference for clean_email
        if user is not None:
            self.initial.setdefault("first_name", getattr(user, "first_name", ""))
            self.initial.setdefault("last_name", getattr(user, "last_name", ""))
            self.initial.setdefault("email", getattr(user, "email", ""))
        if profile is not None:
            self.initial.setdefault("phone", getattr(profile, "phone", ""))
            self.initial.setdefault("location", getattr(profile, "location", ""))
            # farm_size_ha is auto-computed, not set from form
            self.initial.setdefault("notes", getattr(profile, "notes", ""))

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if not email:
            raise django_forms.ValidationError("Email is required.")
        # Reject if another user already owns this email
        qs = User.objects.filter(email__iexact=email)
        if self._user:
            qs = qs.exclude(pk=self._user.pk)
        if qs.exists():
            raise django_forms.ValidationError("This email address is already in use by another account.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if phone and not django_forms.CharField().to_python(phone):
            raise django_forms.ValidationError("Enter a valid phone number.")
        # Allow digits, spaces, +, -, ()
        import re
        if phone and not re.fullmatch(r'[\d\s\+\-\(\)]{6,20}', phone):
            raise django_forms.ValidationError("Enter a valid phone number (6–20 digits, spaces, +, -, () allowed).")
        return phone

    def save(self, user: User, profile: Profile):
        if self.is_valid():
            data = self.cleaned_data
            user.first_name = data.get("first_name") or ""
            user.last_name = data.get("last_name") or ""
            user.email = data.get("email") or ""
            user.save()

            profile.phone = data.get("phone") or ""
            profile.location = data.get("location") or ""
            profile.notes = data.get("notes") or ""
            profile.save()
            return user, profile
        return None


class KnowledgeEntryForm(forms.ModelForm):
    """Form for creating/editing pest/disease knowledge base entries."""

    class Meta:
        model = KnowledgeBaseEntry
        fields = [
            "name",
            "category",
            "description",
            "symptoms",
            "causes",
            "prevention",
            "image",
            "is_published",
        ]
        labels = {
            "name": "Name",
            "category": "Category",
            "description": "Overview / description",
            "symptoms": "Symptoms",
            "causes": "Possible causes",
            "prevention": "Prevention",
            "image": "Image",
            "is_published": "Published",
        }
        help_texts = {
            "name": "e.g. Rice Blast, Brown Planthopper, Nitrogen Deficiency",
            "category": "Type of categories.",
            "description": "Short overview of what this is.",
            "symptoms": "List key signs farmers should look for.",
            "causes": "Common triggers or environmental conditions.",
            "prevention": "How to avoid this issue in the future.",
            "image": "Optional: upload a symptom photo to help identification.",
            "is_published": "If unchecked, only admins/technicians can see this entry.",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "category": forms.Select(attrs={"class": INPUT_CLASS}),
            "description": forms.Textarea(attrs={"class": INPUT_CLASS + " resize-y", "rows": 3}),
            "symptoms": forms.Textarea(attrs={"class": INPUT_CLASS + " resize-y", "rows": 3}),
            "causes": forms.Textarea(attrs={"class": INPUT_CLASS + " resize-y", "rows": 3}),
            "prevention": forms.Textarea(attrs={"class": INPUT_CLASS + " resize-y", "rows": 3}),
            "image": forms.ClearableFileInput(attrs={"class": INPUT_CLASS}),
            "is_published": forms.CheckboxInput(attrs={"class": "h-4 w-4 text-blue-600 border-gray-300 rounded"}),
        }

    def clean_name(self):
        """Ensure the entry has non-empty name."""
        name = self.cleaned_data.get("name", "").strip()
        if not name:
            raise forms.ValidationError("Please provide a name for this knowledge entry.")
        return name


class FieldForm(forms.ModelForm):
    """
    Form for creating and editing Field records.
    BEST PRACTICE: 
    - Admin/Technician can search and select field owner (searchable dropdown)
    - Barangay is text input for flexibility (users can type any barangay name)
    """
    
    # Add owner field with searchable widget (not in Meta because it's added conditionally)
    owner = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=True,
        label='Field Owner (User)',
        help_text='Search by name or username',
        widget=forms.Select(attrs={
            'class': INPUT_CLASS,
            'data-searchable': 'true',  # For JS enhancement
        })
    )
    
    class Meta:
        from .models import Field
        model = Field
        fields = [
            'name',
            'area_hectares',
            'barangay',
            'municipality',
            'province',
            'soil_type',
            'ecosystem_type',
            'flood_prone',
            'gps_lat',
            'gps_lon',
        ]
        labels = {
            'name': 'Field Name',
            'area_hectares': 'Area (hectares)',
            'barangay': 'Barangay',
            'municipality': 'Municipality',
            'province': 'Province',
            'soil_type': 'Soil Type',
            'ecosystem_type': 'Ecosystem Type',
            'flood_prone': 'Flood Prone',
            'gps_lat': 'GPS Latitude',
            'gps_lon': 'GPS Longitude',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g., North Field'}),
            'area_hectares': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0.01', 'placeholder': '0.00'}),
            'barangay': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g., San Jose'}),
            'municipality': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g., Malaybalay'}),
            'province': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'e.g., Bukidnon'}),
            'soil_type': forms.Select(attrs={'class': INPUT_CLASS}),
            'ecosystem_type': forms.Select(attrs={'class': INPUT_CLASS}),
            'flood_prone': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded'}),
            'gps_lat': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.000001', 'placeholder': 'e.g., 14.123456'}),
            'gps_lon': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.000001', 'placeholder': 'e.g., 121.123456'}),
        }
        help_texts = {
            'name': 'A unique name for this field',
            'area_hectares': 'Total field area in hectares',
            'barangay': 'Type the barangay name (optional)',
            'municipality': 'Municipality (optional)',
            'province': 'Province (optional)',
            'soil_type': 'Primary soil texture (optional)',
            'ecosystem_type': 'Field ecosystem type (optional)',
            'flood_prone': 'Check if this field is prone to flooding',
            'gps_lat': 'GPS coordinates (optional)',
            'gps_lon': 'GPS coordinates (optional)',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        # Get user role
        user_profile = getattr(user, 'profile', None)
        role = user_profile.role if user_profile else 'farmer'
        
        # BEST PRACTICE: Admin/Technician can select owner, Farmer creates for themselves
        if role in ['admin', 'technician']:
            # Show owner selection field for admin/technician
            from .models import Profile
            
            # Get all farmer profiles (and technicians/admins for flexibility)
            farmer_profiles = Profile.objects.select_related('user').filter(
                role__in=['farmer', 'technician', 'admin']
            ).order_by('user__first_name', 'user__last_name', 'user__username')
            
            self.fields['owner'].queryset = farmer_profiles
            
            # Custom label to show full name + username + role
            self.fields['owner'].label_from_instance = lambda obj: (
                f"{obj.user.get_full_name() or obj.user.username} "
                f"(@{obj.user.username}) - {obj.get_role_display()}"
            )
            
            # If editing, set initial owner
            if self.instance and self.instance.pk:
                self.fields['owner'].initial = self.instance.owner
            
            # Reorder fields to show owner first
            field_order = [
                'owner',
                'name',
                'area_hectares',
                'barangay',
                'municipality',
                'province',
                'soil_type',
                'ecosystem_type',
                'flood_prone',
                'gps_lat',
                'gps_lon',
            ]
            self.order_fields(field_order)
            
        else:
            # Farmer: Remove owner field, will be set automatically in view
            del self.fields['owner']
        
        # Make optional fields
        self.fields['barangay'].required = False
        self.fields['municipality'].required = False
        self.fields['province'].required = False
        self.fields['soil_type'].required = False
        self.fields['ecosystem_type'].required = False
        self.fields['flood_prone'].required = False
        self.fields['gps_lat'].required = False
        self.fields['gps_lon'].required = False

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            from .models import Field
            
            # Get the owner to check against
            owner = self.cleaned_data.get('owner')
            
            # For farmers, owner is self.user
            if not owner and self.user:
                from .models import Profile
                owner = Profile.objects.filter(user=self.user).first()
            
            if owner:
                # Check for duplicate field name for this owner
                qs = Field.objects.filter(owner=owner, name__iexact=name)
                if self.instance.pk:
                    qs = qs.exclude(pk=self.instance.pk)
                if qs.exists():
                    owner_display = owner.user.get_full_name() or owner.user.username
                    raise forms.ValidationError(
                        f'"{owner_display}" already has a field named "{name}". '
                        f'Please choose a different name.'
                    )
        return name

    def clean(self):
        cleaned_data = super().clean()
        gps_lat = cleaned_data.get('gps_lat')
        gps_lon = cleaned_data.get('gps_lon')
        
        # Both GPS coordinates should be provided together or both empty
        if (gps_lat is not None and gps_lon is None) or (gps_lat is None and gps_lon is not None):
            raise forms.ValidationError('Please provide both latitude and longitude, or leave both empty.')
        
        return cleaned_data


class PlantingRecordForm(forms.ModelForm):
    """Form for creating and editing PlantingRecord records."""

    # Admin/Tech only: filter field dropdown by owner
    owner_filter = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label='Field Owner (User)',
        help_text='Search by name or username — only their fields will appear below',
        widget=forms.Select(attrs={
            'class': INPUT_CLASS,
            'data-searchable': 'true',
            'id': 'id_owner_filter',
        }),
    )

    class Meta:
        from .models import PlantingRecord
        model = PlantingRecord
        fields = [
            'field',
            'variety',
            'season',
            'planting_method',
            'area_planted_ha',
            'seed_rate_kg_per_ha',
            'planting_date',
            'expected_harvest_date',
            'actual_harvest_date',
            'status',
            'notes',
        ]
        labels = {
            'field': 'Field',
            'variety': 'Rice Variety',
            'season': 'Season',
            'planting_method': 'Planting Method',
            'area_planted_ha': 'Area Planted (ha)',
            'seed_rate_kg_per_ha': 'Seed Rate (kg/ha)',
            'planting_date': 'Planting Date',
            'expected_harvest_date': 'Expected Harvest Date',
            'actual_harvest_date': 'Actual Harvest Date',
            'status': 'Status',
            'notes': 'Notes',
        }
        widgets = {
            'field': forms.Select(attrs={'class': INPUT_CLASS}),
            'variety': forms.Select(attrs={'class': INPUT_CLASS}),
            'season': forms.Select(attrs={'class': INPUT_CLASS}),
            'planting_method': forms.Select(attrs={'class': INPUT_CLASS}),
            'area_planted_ha': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0.01', 'placeholder': '0.00'}),
            'seed_rate_kg_per_ha': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0', 'placeholder': 'e.g. 50'}),
            'planting_date': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'expected_harvest_date': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'actual_harvest_date': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'status': forms.Select(attrs={'class': INPUT_CLASS}),
            'notes': forms.Textarea(attrs={'class': INPUT_CLASS + ' resize-none', 'rows': 3, 'placeholder': 'Optional notes about this planting cycle'}),
        }
        help_texts = {
            'field': 'Select the field for this planting',
            'variety': 'Select the rice variety planted',
            'season': 'Wet or dry season for this planting',
            'planting_method': 'How the crop was planted',
            'area_planted_ha': 'Area planted in hectares (must be <= field size)',
            'seed_rate_kg_per_ha': 'Estimated seed rate per hectare (optional)',
            'planting_date': 'Date when rice was planted',
            'expected_harvest_date': 'Expected harvest date (auto-calculated if variety has growth duration)',
            'actual_harvest_date': 'Actual harvest date (set automatically when a harvest record is created)',
            'status': 'Current status of this planting cycle',
            'notes': 'Optional notes about this planting cycle',
        }

    def __init__(self, *args, user=None, target_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        # Check if this is an edit (instance exists) or create (new)
        is_editing = self.instance and self.instance.pk

        # Filter fields to only show user's fields
        if user:
            from .models import Field, PlantingRecord, Profile

            # Get user profile and role
            user_profile = getattr(user, 'profile', None)
            role = user_profile.role if user_profile else 'farmer'

            if role in ['admin', 'technician']:
                # Populate the owner_filter dropdown with all selectable profiles
                farmer_profiles = Profile.objects.select_related('user').filter(
                    role__in=['farmer', 'technician', 'admin'],
                    user__is_active=True,
                ).order_by('user__first_name', 'user__last_name', 'user__username')
                self.fields['owner_filter'].queryset = farmer_profiles
                self.fields['owner_filter'].label_from_instance = lambda obj: (
                    f"{obj.user.get_full_name() or obj.user.username} "
                    f"(@{obj.user.username}) — {obj.get_role_display()}"
                )
                # Pre-select the target_profile in the dropdown
                if target_profile:
                    self.fields['owner_filter'].initial = target_profile
                    # Filter the field queryset to only this profile's fields
                    all_fields = Field.objects.filter(
                        owner=target_profile, is_active=True,
                    ).select_related('owner', 'owner__user').order_by('name')
                else:
                    all_fields = Field.objects.filter(
                        is_active=True,
                    ).select_related('owner', 'owner__user').order_by('name')
            else:
                # Farmer: remove the owner_filter field entirely
                del self.fields['owner_filter']
                all_fields = Field.objects.filter(owner__user=user).order_by('name')
            
            if is_editing:
                # BEST PRACTICE: When editing, make field READ-ONLY
                # Field cannot be changed because it has related data (detections, yields, etc.)
                self.fields['field'].disabled = True
                self.fields['field'].queryset = all_fields
                self.fields['field'].help_text = (
                    '⚠️ Field cannot be changed for existing planting records. '
                    'This protects data integrity of related detections and yield predictions.'
                )
                # Add visual styling to indicate it's disabled
                self.fields['field'].widget.attrs.update({
                    'class': INPUT_CLASS + ' bg-gray-100 cursor-not-allowed',
                    'readonly': 'readonly',
                })
            else:
                # When creating NEW planting, keep field choices broad.
                # Yearly 3-cycle enforcement depends on the selected planting_date,
                # so we validate it in clean() using field + planting_date.year.
                self.fields['field'].queryset = all_fields
                self.fields['field'].help_text = (
                    'Select the field for this planting. '
                    'Maximum of 3 planting cycles per field per selected year is enforced on save.'
                )
        
        # Make notes and expected_harvest_date optional
        self.fields['notes'].required = False
        self.fields['expected_harvest_date'].required = False

        # Only show active (non-archived) varieties in the dropdown
        self.fields['variety'].queryset = RiceVariety.objects.filter(is_active=True).order_by('code')

    def clean(self):
        cleaned_data = super().clean()
        field = cleaned_data.get('field')
        planting_date = cleaned_data.get('planting_date')
        expected_harvest_date = cleaned_data.get('expected_harvest_date')
        
        # Validate harvest date is after planting date
        if planting_date and expected_harvest_date:
            if expected_harvest_date <= planting_date:
                raise forms.ValidationError('Expected harvest date must be after the planting date.')
        
        # Validate na hindi masyadong malayo sa nakaraan ang planting_date
        if planting_date:
            from django.utils import timezone
            from . import services

            today = timezone.now().date()
            allowed_days = services.get_allowed_past_days_for_planting()

            # Tagalog:
            # - Kapag negative ang value (hindi inaasahan), i-treat bilang 0 (today only) para safe.
            if allowed_days < 0:
                allowed_days = 0

            min_allowed_date = today - timezone.timedelta(days=allowed_days)

            if planting_date < min_allowed_date:
                raise forms.ValidationError(
                    f'Planting date is too far in the past. '
                    f'Currently, admin allows only up to {allowed_days} day(s) back from today.'
                )
        
        # Ensure required selections are present (some fields are nullable in the database for legacy records)
        if not cleaned_data.get('variety'):
            self.add_error('variety', 'Please select a rice variety.')
        if not cleaned_data.get('season'):
            self.add_error('season', 'Please select a season.')
        if not cleaned_data.get('planting_method'):
            self.add_error('planting_method', 'Please select a planting method.')

        # Validate planted area (must be positive & within field size)
        area_planted = cleaned_data.get('area_planted_ha')
        if area_planted is not None and field and field.area_hectares is not None:
            if area_planted <= 0:
                self.add_error('area_planted_ha', 'Area planted must be greater than zero.')
            elif area_planted > float(field.area_hectares):
                self.add_error('area_planted_ha', 'Area planted cannot exceed the field size.')

        # Yearly 3-cycle rule is enforced centrally in PlantingRecord.clean().
        # Tagalog: Iwas duplicate logic para walang divergence sa forms/admin/API.
        
        return cleaned_data


class AdminUserCreationForm(forms.Form):
    """Form for admin-only creation of farmer and technician users"""

    _INPUT = 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition bg-white'
    _SELECT = 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition bg-white'

    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('technician', 'Technician'),
    ]

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'e.g. juan.dela.cruz', 'autocomplete': 'off'}),
        help_text='150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': _INPUT, 'placeholder': 'e.g. juan@example.com', 'autocomplete': 'off'}),
        help_text='Enter a valid email address.'
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': _INPUT, 'autocomplete': 'new-password'}),
        help_text='Must be at least 8 characters.'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': _INPUT, 'autocomplete': 'new-password'}),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': _SELECT}),
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Last name'})
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'e.g. 09171234567'}),
    )
    location = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Barangay, Municipality'}),
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Passwords do not match.')
            if len(password1) < 8:
                raise forms.ValidationError('Password must be at least 8 characters.')
        
        return password2
    
    def save(self):
        """
        Create new User and Profile with specified role.
        
        Note: Profile is auto-created by signal, but we update it with form data.
        """
        from .models import Profile
        
        # Create user (signal will auto-create profile with 'farmer' role)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data.get('first_name', ''),
            last_name=self.cleaned_data.get('last_name', '')
        )
        
        # Update the auto-created profile with form data
        profile = user.profile
        profile.role = self.cleaned_data['role']
        profile.phone = self.cleaned_data.get('phone', '')
        profile.location = self.cleaned_data.get('location', '')
        profile.save()
        
        return user


class AdminUserEditForm(forms.Form):
    """Form for admin to edit existing user accounts - BEST PRACTICE"""

    _INPUT = 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition bg-white'
    _SELECT = 'w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition bg-white'
    _INPUT_DISABLED = 'w-full px-3 py-2 text-sm border border-gray-200 rounded-lg bg-gray-50 text-gray-500 cursor-not-allowed'
    _CHECKBOX = 'w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer'

    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('technician', 'Technician'),
        ('admin', 'Administrator'),
    ]

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': _INPUT_DISABLED, 'readonly': 'readonly'}),
        help_text='Username cannot be changed for security reasons.'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': _INPUT}),
        help_text='User email address.'
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': _INPUT})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': _INPUT})
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': _SELECT}),
        help_text='Change user role (farmer, technician, or admin).'
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': _INPUT}),
        help_text='Contact phone number.'
    )
    location = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': _INPUT}),
        help_text='User location or assigned area.'
    )
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': _CHECKBOX}),
        help_text='Uncheck to deactivate account (user cannot login).'
    )
    is_approved = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': _CHECKBOX}),
        help_text='Check to approve pending farmer registration.'
    )
    reset_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': _INPUT,
            'placeholder': 'Leave blank to keep current password',
            'autocomplete': 'new-password',
        }),
        help_text='Enter new password to reset, or leave blank to keep current password.'
    )
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        
        if user:
            # Pre-fill form with existing data
            self.fields['username'].initial = user.username
            self.fields['email'].initial = user.email
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['is_active'].initial = user.is_active
            
            if hasattr(user, 'profile'):
                self.fields['role'].initial = user.profile.role
                self.fields['phone'].initial = user.profile.phone
                self.fields['location'].initial = user.profile.location
                self.fields['is_approved'].initial = user.profile.is_approved
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check if email is taken by another user
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('This email is already registered by another user.')
        return email
    
    def clean_reset_password(self):
        password = self.cleaned_data.get('reset_password')
        if password and len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters.')
        return password
    
    def save(self):
        """Update user and profile with form data."""
        from .models import Profile
        
        # Update user fields
        self.user.email = self.cleaned_data['email']
        self.user.first_name = self.cleaned_data.get('first_name', '')
        self.user.last_name = self.cleaned_data.get('last_name', '')
        self.user.is_active = self.cleaned_data.get('is_active', False)
        
        # Reset password if provided
        reset_password = self.cleaned_data.get('reset_password')
        if reset_password:
            self.user.set_password(reset_password)
        
        self.user.save()
        
        # Update profile
        profile, _ = Profile.objects.get_or_create(user=self.user)
        profile.role = self.cleaned_data['role']
        profile.phone = self.cleaned_data.get('phone', '')
        profile.location = self.cleaned_data.get('location', '')
        profile.is_approved = self.cleaned_data.get('is_approved', True)
        profile.save()
        
        return self.user


class CustomPasswordChangeForm(PasswordChangeForm):
    """
    Custom password change form with improved styling and validation.
    BEST PRACTICES:
    - Requires old password verification (security)
    - Strong password validation (Django's built-in validators)
    - Consistent UI with the rest of the application
    - Clear error messages for users
    """
    
    old_password = django_forms.CharField(
        label="Current Password",
        strip=False,
        widget=django_forms.PasswordInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Enter your current password',
            'autocomplete': 'current-password',
        }),
        help_text="Enter your current password for verification."
    )
    
    new_password1 = django_forms.CharField(
        label="New Password",
        strip=False,
        widget=django_forms.PasswordInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Enter new password',
            'autocomplete': 'new-password',
        }),
        help_text=(
            "Your password must contain at least 8 characters and cannot be entirely numeric."
        )
    )
    
    new_password2 = django_forms.CharField(
        label="Confirm New Password",
        strip=False,
        widget=django_forms.PasswordInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Confirm new password',
            'autocomplete': 'new-password',
        }),
        help_text="Enter the same password as before, for verification."
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom styling to error messages
        for field in self.fields.values():
            field.error_messages = {
                'required': 'This field is required.',
            }


# Treatment Management Forms
class TreatmentRecommendationForm(forms.ModelForm):
    """Form for creating and editing treatment recommendations."""

    knowledge_entries = forms.ModelMultipleChoiceField(
        queryset=KnowledgeBaseEntry.objects.filter(is_active=True, is_published=True),
        required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm',
            'size': '6',
            'data-searchable': 'true',
        }),
        help_text=(
            'Pumili lang ng naka-publish na Knowledge entries. ' 
            'Hindi puwedeng i-link ang draft/unpublished entries sa treatment.'
        ),
    )

    class Meta:
        model = TreatmentRecommendation
        fields = [
            'disease',
            'severity_min',
            'severity_max',
            'short_text',
            'detailed_text',
            'knowledge_entries',
            'factors_favoring',
            'factor_actions',
            'factor_expected_results',
            'cultural_practices',
            'chemical_control',
            'severity_threshold',
            'severity_high_msg',
            'priority',
            'is_active',
        ]
        widgets = {
            'disease': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm'
            }),
            'severity_min': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm',
                'min': '0',
                'max': '100'
            }),
            'severity_max': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm',
                'min': '0',
                'max': '100'
            }),
            'short_text': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm',
                'placeholder': 'Quick summary for mobile/dashboard (max 200 characters)...',
                'maxlength': '200'
            }),
            'detailed_text': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm',
                'rows': '3',
                'placeholder': 'Full detailed treatment instructions...'
            }),
            'knowledge_entries': forms.SelectMultiple(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm',
                'size': '6',
                'data-searchable': 'true',
            }),
            'factors_favoring': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm',
                'rows': '4',
                'placeholder': 'Environmental conditions and factors...'
            }),
            'factor_actions': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-green-300 bg-green-50 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm',
                'rows': '4',
                'placeholder': 'One quick action per line, same order as Factors above...'
            }),
            'factor_expected_results': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-blue-300 bg-blue-50 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm',
                'rows': '4',
                'placeholder': 'One expected result per line, same order as Factors above...'
            }),
            'cultural_practices': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm',
                'rows': '4',
                'placeholder': 'Cultural and agronomic practices...'
            }),
            'chemical_control': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm',
                'rows': '4',
                'placeholder': 'Chemical treatment options (use as last resort)...'
            }),
            'preventive_measures': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500 sm:text-sm',
                'rows': '4',
                'placeholder': 'Preventive measures and best practices...'
            }),
            'severity_threshold': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-orange-300 bg-orange-50 shadow-sm focus:border-orange-500 focus:ring-orange-500 sm:text-sm',
                'min': '1',
                'max': '100',
            }),
            'severity_high_msg': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-orange-300 bg-orange-50 shadow-sm focus:border-orange-500 focus:ring-orange-500 sm:text-sm',
                'rows': '3',
                'placeholder': 'IPM-based escalation message when severity ≥ threshold (e.g. "At this severity level, cultural control alone is insufficient. Apply recommended fungicide per DA guidelines and consult your local technician.")...'
            }),
            'priority': forms.NumberInput(attrs={
                'type': 'range',
                'class': 'mt-1 block w-full h-2 rounded-full accent-green-600 cursor-pointer',
                'min': '1',
                'max': '10',
                'step': '1',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded'
            }),
        }
        labels = {
            'disease': 'Disease Type',
            'severity_min': 'Minimum Severity (%)',
            'severity_max': 'Maximum Severity (%)',
            'short_text': 'Quick Summary',
            'detailed_text': 'Detailed Instructions',
            'knowledge_entries': 'Knowledge Entry References',
            'factors_favoring': 'Factors Favoring Disease',
            'factor_actions': 'Quick Actions (per factor)',
            'factor_expected_results': 'Expected Results (per factor)',
            'cultural_practices': 'Cultural Practices (IPM - Integrated Pest Management - First Line)',
            'chemical_control': 'Chemical Control (Last Resort)',
            'preventive_measures': 'Preventive Measures',
            'severity_threshold': 'Severity Escalation Threshold (%)',
            'severity_high_msg': 'Escalation Message (shown when severity ≥ threshold)',
            'priority': 'Priority (1-10: 1=least critical, 10=most severe/critical)',
            'is_active': 'Active',
        }
        help_texts = {
            'severity_min': 'The minimum severity percentage for this treatment (e.g., 0 for mild)',
            'severity_max': 'The maximum severity percentage for this treatment (e.g., 30 for mild, 100 for severe)',
            'short_text': 'Brief summary shown in detection results (max 200 characters)',
            'detailed_text': 'Full detailed treatment instructions',
            'knowledge_entries': 'Link one or more Knowledge entries. The detection detail page draws symptoms/causes/prevention from these entries only.',
            'cultural_practices': 'Emphasize non-chemical Integrated Pest Management practices first (crop rotation, resistant varieties, biological control, etc.)',
            'chemical_control': 'Only recommend when absolutely necessary, include dosage and safety warnings',
            'priority': 'Scale 1-10 where: 1-3=Low priority (mild), 4-7=Medium priority (moderate), 8-10=High priority (severe/critical)',
            'severity_threshold': 'Set based on IPM principles. Example: 40% for high-priority diseases (Neck Blast), 70% for low-priority (Leaf Scald). Below this threshold, factor checkboxes alone are sufficient.',
            'severity_high_msg': 'Write an IPM-based message explaining what to do when cultural control is no longer sufficient. Leave blank to hide the severity escalation line.',
        }


class AnnouncementForm(forms.ModelForm):
    """Form for creating and editing announcements"""

    publish_timing = forms.ChoiceField(
        choices=[
            ('immediate', 'Immediate Publish'),
            ('scheduled', 'Scheduled Publish'),
        ],
        required=False,
        initial='immediate',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
        }),
        label='Publishing Mode',
        help_text='Choose Immediate to publish now, or Scheduled to publish at a specific date/time.',
    )
    
    class Meta:
        from .models import Announcement
        model = Announcement
        fields = [
            'title',
            'content',
            'category',
            'target_audience',
            'target_barangay',
            'target_user',
            'priority',
            'published_at',
            'expires_at',
            'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'placeholder': 'e.g., ⚠️ Brown Spot Alert in San Nicolas',
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'rows': 8,
                'placeholder': 'Enter full announcement details...\n\nYou can use:\n- Bullet points\n- Multiple paragraphs\n- Clear formatting',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
            }),
            'target_audience': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'onchange': 'toggleTargetFields(this.value)',
            }),
            'target_barangay': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'data-searchable': 'true',
            }),
            'target_user': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'data-searchable': 'true',
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
            }),
            'published_at': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'datetime-local',
                'step': '1',  # BEST PRACTICE: Include seconds in datetime picker
            }),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'type': 'datetime-local',
                'step': '1',  # BEST PRACTICE: Include seconds in datetime picker
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded',
            }),
        }
        labels = {
            'title': 'Announcement Title',
            'content': 'Full Message',
            'category': 'Category',
            'target_audience': 'Who should see this?',
            'target_barangay': 'Select Barangay',
            'target_user': 'Select User',
            'priority': 'Priority Level',
            'published_at': 'Publish Date & Time',
            'expires_at': 'Expiration Date (Optional)',
            'is_active': 'Active (Published)',
        }
        help_texts = {
            'title': 'Short, descriptive title (e.g., "⚠️ Brown Spot Alert"). You can use emojis!',
            'content': 'Full announcement message. Use line breaks for better readability.',
            'category': 'Select the type of announcement to help users filter',
            'target_audience': 'Choose who will receive this announcement',
            'target_barangay': 'Only shown if "Specific Barangay" is selected above',
            'target_user': 'Only shown if "Specific User" is selected above',
            'priority': '📘 Info = General | 📗 Announcement = Tips | 📙 Warning = Important | 📕 Urgent = Critical',
            'published_at': 'Leave empty to publish immediately, or schedule for future',
            'expires_at': 'Announcement will auto-hide after this date (optional)',
            'is_active': 'Uncheck to save as draft without publishing',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        from django.utils import timezone
        
        # Get current time in local timezone (Asia/Manila)
        current_time = timezone.localtime(timezone.now())
        
        # For new forms, default to immediate mode (empty published_at).
        if not self.instance.pk:
            self.initial.setdefault('publish_timing', 'immediate')
            self.initial.setdefault('published_at', '')
        elif self.instance.published_at:
            self.initial['publish_timing'] = 'scheduled'
        else:
            self.initial['publish_timing'] = 'immediate'
        
        # BEST PRACTICE: Set min attribute to current datetime (with seconds) to prevent past dates
        self.fields['published_at'].widget.attrs['min'] = current_time.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Make target fields not required (we'll validate conditionally)
        self.fields['target_barangay'].required = False
        self.fields['target_user'].required = False
        
        # BEST PRACTICE: Get barangays from actual Field records (not separate Barangay model)
        # This ensures we only show barangays that have active fields
        from .models import Field
        from django.db.models import Q
        
        # Get distinct barangay names from Field model (exclude null/empty)
        barangay_names = Field.objects.filter(
            Q(barangay__isnull=False) & ~Q(barangay='')
        ).values_list('barangay', flat=True).distinct().order_by('barangay')
        
        # Convert to choices format: (value, display_label)
        barangay_choices = [('', '-- Select Barangay --')] + [(name, name) for name in barangay_names]
        
        # Update the field to use ChoiceField instead of ModelChoiceField
        self.fields['target_barangay'] = forms.ChoiceField(
            choices=barangay_choices,
            required=False,
            widget=forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
                'data-searchable': 'true',
            }),
            label='Select Barangay',
            help_text='Only shown if "Specific Barangay" is selected above'
        )
        
        # Keep user selection with Profile queryset
        self.fields['target_user'].queryset = Profile.objects.select_related('user').order_by('user__username')
        
        # Show username, role, and email in target user dropdown labels.
        self.fields['target_user'].label_from_instance = lambda obj: (
            f"{obj.user.username} ({obj.get_role_display()}) - {obj.user.email}"
            if obj.user.email else f"{obj.user.username} ({obj.get_role_display()})"
        )
    
    def clean(self):
        """Validate announcement form data with timezone-aware datetime checks."""
        cleaned_data = super().clean()
        target_audience = cleaned_data.get('target_audience')
        target_barangay = cleaned_data.get('target_barangay')
        target_user = cleaned_data.get('target_user')
        published_at = cleaned_data.get('published_at')
        expires_at = cleaned_data.get('expires_at')
        publish_timing = cleaned_data.get('publish_timing')

        if publish_timing == 'immediate':
            cleaned_data['published_at'] = None
            published_at = None
        elif publish_timing == 'scheduled' and not published_at:
            self.add_error('published_at', 'Please set a publish date/time for scheduled announcements.')
        
        # Validate target fields based on audience selection
        if target_audience == 'barangay' and not target_barangay:
            self.add_error('target_barangay', 'Please select a barangay for this announcement.')
        
        if target_audience == 'user' and not target_user:
            self.add_error('target_user', 'Please select a specific user for this announcement.')
        
        # BEST PRACTICE: Timezone-aware validation to prevent scheduling in the past
        if published_at:
            from django.utils import timezone
            
            # Get current time in the configured timezone (Asia/Manila)
            now = timezone.now()
            
            # Ensure published_at is timezone-aware
            if timezone.is_naive(published_at):
                published_at = timezone.make_aware(published_at)
                cleaned_data['published_at'] = published_at
            
            # Only validate for new announcements or if changing the publish date
            if not self.instance.pk or (self.instance.pk and self.instance.published_at != published_at):
                if published_at < now:
                    time_diff = (now - published_at).total_seconds()
                    if time_diff < 60:
                        self.add_error('published_at', 'Cannot schedule announcement in the past. Please select current or future date/time.')
                    elif time_diff < 3600:
                        minutes = int(time_diff / 60)
                        self.add_error('published_at', f'This time is {minutes} minute(s) in the past. Please select a future date/time.')
                    else:
                        hours = int(time_diff / 3600)
                        self.add_error('published_at', f'This date is {hours} hour(s) in the past. Please select a future date/time.')
        
        # BEST PRACTICE: Expiration must be after publish date
        if published_at and expires_at:
            # Ensure expires_at is timezone-aware
            if timezone.is_naive(expires_at):
                expires_at = timezone.make_aware(expires_at)
                cleaned_data['expires_at'] = expires_at
            
            if expires_at <= published_at:
                time_diff = (published_at - expires_at).total_seconds()
                if time_diff < 3600:
                    minutes = int(time_diff / 60)
                    self.add_error('expires_at', f'Expiration must be after publish date (currently {minutes} minute(s) before publish).')
                else:
                    hours = int(time_diff / 3600)
                    self.add_error('expires_at', f'Expiration must be after publish date (currently {hours} hour(s) before publish).')
        
        return cleaned_data


# ── Shared Tailwind CSS widget classes (used by RiceVarietyForm, SeasonLogForm, FarmActivityForm) ──
_INPUT    = "w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent"
_SELECT   = "w-full px-4 py-2 border border-gray-300 rounded-lg text-sm bg-white focus:ring-2 focus:ring-green-500 focus:border-transparent"
_TEXTAREA = "w-full px-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent resize-y min-h-[80px]"


class RiceVarietyForm(forms.ModelForm):
    """
    Complete form for creating and editing rice variety records.
    Grouped into 7 logical sections for easy data entry.
    """

    class Meta:
        model  = RiceVariety
        fields = [
            # 1. Variety Identification — pangunahing pagkakakilanlan
            'code', 'name', 'variety_type', 'release_year', 'developer',
            # 2. Agronomic Characteristics — biological traits
            'average_growth_days', 'plant_height_cm', 'tillering_capacity',
            'grain_type', 'lodging_resistance',
            # 3. Environmental Adaptation — saan angkop ang variety
            'climate_type', 'soil_type_compatibility',
            'flood_tolerance', 'drought_tolerance', 'temperature_tolerance',
            # 4. Yield Characteristics — performance ng variety
            'average_yield_t_ha', 'potential_yield_t_ha', 'grain_quality',
            # 5. Pest and Disease Resistance — resistansya sa sakit (aligned sa 14 CNN classes)
            'blast_resistance', 'neck_blast_resistance',
            'blight_resistance', 'brown_spot_resistance',
            'false_smut_resistance', 'leaf_scald_resistance',
            'leaf_smut_resistance', 'narrow_brown_spot_resistance',
            'rice_hispa_resistance', 'sheath_blight_resistance',
            'tungro_resistance', 'unhealthy_flowers_resistance',
            # 6. Seed Management — kalidad ng binhi
            'seed_source', 'seed_certification', 'germination_rate_pct',
            # 7. Management Recommendations — gabay para sa magsasaka
            'fertilizer_schedule', 'water_management',
            'plant_spacing_cm', 'planting_season',
            # Extra
            'notes',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ── Section 1: Variety Identification ─────────────────────────
        self.fields['code'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. RC222, NSIC Rc222', 'maxlength': '20'
        })
        self.fields['name'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. RC Masipag 222', 'maxlength': '120'
        })
        # Dropdown with blank placeholder for required selects
        self.fields['variety_type'].widget = forms.Select(attrs={'class': _SELECT})
        self.fields['variety_type'].choices = [('', '— Select Variety Type —')] + list(RiceVariety.VarietyType.choices)
        self.fields['release_year'].widget = forms.NumberInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. 2012', 'min': '1900', 'max': '2100'
        })
        self.fields['developer'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. PhilRice, IRRI, DA-RFU'
        })

        # ── Section 2: Agronomic Characteristics ──────────────────────
        self.fields['average_growth_days'].widget = forms.NumberInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. 115', 'min': '60', 'max': '365'
        })
        self.fields['plant_height_cm'].widget = forms.NumberInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. 95', 'min': '1', 'max': '300'
        })
        self.fields['tillering_capacity'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. High, Moderate, Low'
        })
        self.fields['grain_type'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. Long slender, Medium bold'
        })
        self.fields['lodging_resistance'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. Good, Moderate, Poor'
        })

        # ── Section 3: Environmental Adaptation ───────────────────────
        self.fields['climate_type'].widget = forms.Select(attrs={'class': _SELECT})
        self.fields['climate_type'].choices = [('', '— Select Climate Type —')] + list(RiceVariety.ClimateType.choices)
        self.fields['soil_type_compatibility'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. Clay loam, Sandy loam, All soil types'
        })
        self.fields['flood_tolerance'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. Tolerant, Moderately tolerant, Susceptible'
        })
        self.fields['drought_tolerance'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. Tolerant, Susceptible'
        })
        self.fields['temperature_tolerance'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. Tolerant to high temperature'
        })

        # ── Section 4: Yield Characteristics ──────────────────────────
        self.fields['average_yield_t_ha'].widget = forms.NumberInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. 5.5', 'min': '0', 'max': '20', 'step': '0.01'
        })
        self.fields['potential_yield_t_ha'].widget = forms.NumberInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. 8.0', 'min': '0', 'max': '30', 'step': '0.01'
        })
        self.fields['grain_quality'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. Premium, Good milling quality'
        })

        # ── Section 5: Pest & Disease Resistance ──────────────────────
        # Blank option "— Not Assessed —" for all 12 CNN-aligned resistance fields
        _RESISTANCE_CHOICES = [('', '— Not Assessed —')] + list(RiceVariety.ResistanceLevel.choices)
        for field in [
            'blast_resistance', 'neck_blast_resistance',
            'blight_resistance', 'brown_spot_resistance',
            'false_smut_resistance', 'leaf_scald_resistance',
            'leaf_smut_resistance', 'narrow_brown_spot_resistance',
            'rice_hispa_resistance', 'sheath_blight_resistance',
            'tungro_resistance', 'unhealthy_flowers_resistance',
        ]:
            self.fields[field].widget = forms.Select(attrs={'class': _SELECT})
            self.fields[field].choices = _RESISTANCE_CHOICES
            self.fields[field].required = False

        # ── Section 6: Seed Management ────────────────────────────────
        self.fields['seed_source'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. PhilRice Seed Unit, DA-RFU'
        })
        self.fields['seed_certification'].widget = forms.Select(attrs={'class': _SELECT})
        self.fields['seed_certification'].choices = [('', '— Not specified —')] + list(RiceVariety.CertificationLevel.choices)
        self.fields['seed_certification'].required = False
        self.fields['germination_rate_pct'].widget = forms.NumberInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. 95', 'min': '0', 'max': '100'
        })

        # ── Section 7: Management Recommendations ─────────────────────
        self.fields['fertilizer_schedule'].widget = forms.Textarea(attrs={
            'class': _TEXTAREA, 'placeholder': 'e.g. Basal: 30-10-10 kg NPK/ha; 25 DAT: 30 kg N/ha'
        })
        self.fields['water_management'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. Intermittent irrigation, AWD (Alternate Wetting & Drying)'
        })
        self.fields['plant_spacing_cm'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. 20×20 cm, 25×25 cm'
        })
        self.fields['planting_season'].widget = forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. Wet season (Jun–Aug), Dry season (Dec–Feb)'
        })
        self.fields['notes'].widget = forms.Textarea(attrs={
            'class': _TEXTAREA, 'placeholder': 'Additional observations or management recommendations...',
            'rows': '4'
        })

        # ── Mark required/optional ────────────────────────────────────
        # Lahat ng optional fields ay naka-required=False
        optional = [
            'release_year', 'developer', 'plant_height_cm', 'tillering_capacity',
            'grain_type', 'lodging_resistance', 'soil_type_compatibility',
            'flood_tolerance', 'drought_tolerance', 'temperature_tolerance',
            'average_yield_t_ha', 'potential_yield_t_ha', 'grain_quality',
            # Resistance fields — all optional, default to UNKNOWN
            'blast_resistance', 'neck_blast_resistance',
            'blight_resistance', 'brown_spot_resistance',
            'false_smut_resistance', 'leaf_scald_resistance',
            'leaf_smut_resistance', 'narrow_brown_spot_resistance',
            'rice_hispa_resistance', 'sheath_blight_resistance',
            'tungro_resistance', 'unhealthy_flowers_resistance',
            # Seed & management
            'seed_source', 'seed_certification', 'germination_rate_pct',
            'fertilizer_schedule', 'water_management', 'plant_spacing_cm',
            'planting_season', 'notes',
        ]
        for f in optional:
            self.fields[f].required = False

    # ── Validation ────────────────────────────────────────────────────────
    def clean_code(self):
        """I-normalize at i-validate ang variety code."""
        code = self.cleaned_data.get('code', '').strip().upper()
        if not code:
            raise forms.ValidationError('Variety code is required.')
        existing = RiceVariety.objects.filter(code=code)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise forms.ValidationError(f'Variety code "{code}" already exists.')
        return code

    def clean_average_growth_days(self):
        """I-validate na makatotohanan ang growth duration."""
        days = self.cleaned_data.get('average_growth_days')
        if days is None:
            raise forms.ValidationError('Growth duration is required.')
        if days < 60:
            raise forms.ValidationError('Growth duration must be at least 60 days.')
        if days > 365:
            raise forms.ValidationError('Growth duration cannot exceed 365 days.')
        return days

    def clean_germination_rate_pct(self):
        """I-validate na 0-100 ang germination rate."""
        rate = self.cleaned_data.get('germination_rate_pct')
        if rate is not None and not (0 <= rate <= 100):
            raise forms.ValidationError('Germination rate must be between 0 and 100.')
        return rate

    def clean(self):
        """Cross-field validation — average yield dapat hindi mas mataas sa potential."""
        cleaned = super().clean()
        avg = cleaned.get('average_yield_t_ha')
        pot = cleaned.get('potential_yield_t_ha')
        if avg and pot and avg > pot:
            self.add_error(
                'average_yield_t_ha',
                'Average yield cannot be higher than potential yield.'
            )
        return cleaned


# ============================================================================
# SEASON FARM LOG FORMS
# ============================================================================
# Note: _INPUT, _SELECT, _TEXTAREA shared constants are defined above RiceVarietyForm.


class SeasonLogForm(forms.ModelForm):
    """Form for creating/editing a SeasonLog (one season journal per crop cycle)."""

    # Optional: link to an existing PlantingRecord to auto-fill field/variety/dates
    planting = forms.ModelChoiceField(
        queryset=PlantingRecord.objects.none(),
        required=False,
        label='Link to Existing Planting (optional)',
        empty_label='— Or fill manually below —',
        widget=forms.Select(attrs={'class': _SELECT, 'id': 'id_planting_picker'}),
        help_text='Selecting a planting auto-fills Field, Variety, and Dates below.',
    )

    class Meta:
        model  = SeasonLog
        fields = [
            'planting',
            'field', 'variety', 'season_year', 'season_type',
            'date_started', 'date_planted', 'date_harvested',
            'actual_yield_sacks', 'price_per_sack',
            'total_expenses', 'summary_notes',
        ]
        widgets = {
            'field': forms.Select(attrs={
                'class': _SELECT,
            }),
            'variety': forms.Select(attrs={
                'class': _SELECT,
            }),
            'season_year': forms.NumberInput(attrs={
                'class': _INPUT,
                'min': 2000, 'max': 2100,
                'placeholder': 'e.g. 2025',
            }),
            'season_type': forms.Select(attrs={
                'class': _SELECT,
            }),
            'date_started': forms.DateInput(attrs={
                'class': _INPUT, 'type': 'date',
            }),
            'date_planted': forms.DateInput(attrs={
                'class': _INPUT, 'type': 'date',
            }),
            'date_harvested': forms.DateInput(attrs={
                'class': _INPUT, 'type': 'date',
            }),
            'actual_yield_sacks': forms.NumberInput(attrs={
                'class': _INPUT,
                'step': '0.5',
                'placeholder': 'Number of sacks harvested',
            }),
            'price_per_sack': forms.NumberInput(attrs={
                'class': _INPUT,
                'step': '0.01',
                'placeholder': 'Selling price per sack (PHP)',
            }),
            'total_expenses': forms.NumberInput(attrs={
                'class': _INPUT,
                'step': '0.01',
                'placeholder': 'Total season expenses (PHP)',
            }),
            'summary_notes': forms.Textarea(attrs={
                'class': _TEXTAREA,
                'rows': 4,
                'placeholder': 'Overall notes for this season (optional)…',
            }),
        }
        labels = {
            'field':             'Field / Farm',
            'variety':           'Rice Variety',
            'season_year':       'Season Year',
            'season_type':       'Season Type',
            'date_started':      'Season Start Date',
            'date_planted':      'Transplanting / Seeding Date',
            'date_harvested':    'Harvest Date',
            'actual_yield_sacks':'Actual Harvest (sacks)',
            'price_per_sack':    'Selling Price / Sack (PHP)',
            'total_expenses':    'Total Expenses (PHP)',
            'summary_notes':     'Season Notes',
        }

    def __init__(self, *args, owner_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        if owner_profile:
            self.fields['field'].queryset = Field.objects.filter(
                owner=owner_profile, is_active=True
            ).order_by('name')
            # Only show plantings that: belong to profile's fields, are active,
            # and do NOT already have a season log linked
            self.fields['planting'].queryset = PlantingRecord.objects.filter(
                field__owner=owner_profile, is_active=True, season_log__isnull=True
            ).select_related('field', 'variety').order_by('-planting_date')
        self.fields['variety'].queryset = RiceVariety.objects.filter(
            is_active=True
        ).order_by('name')
        self.fields['variety'].required  = False
        self.fields['date_planted'].required  = False
        self.fields['date_harvested'].required = False
        self.fields['actual_yield_sacks'].required = False
        self.fields['price_per_sack'].required  = False
        self.fields['total_expenses'].required = False
        # Default date_started to today if not already set (e.g. on create)
        if not self.initial.get('date_started') and not self.data.get('date_started'):
            from django.utils import timezone
            self.initial['date_started'] = timezone.localdate()


class FarmActivityForm(forms.ModelForm):
    """Form for logging an individual farm activity within a season."""

    class Meta:
        model  = FarmActivity
        fields = [
            'activity_date', 'activity_type', 'title', 'description',
            'input_cost', 'labor_cost',
            'problem_observed', 'problem_severity', 'action_taken',
            'detection_record', 'workers_count',
        ]
        widgets = {
            'activity_date': forms.DateInput(attrs={
                'class': _INPUT, 'type': 'date',
            }),
            'activity_type': forms.Select(attrs={
                'class': _SELECT,
            }),
            'title': forms.TextInput(attrs={
                'class': _INPUT,
                'placeholder': "e.g. Applied Urea 45-0-0, 1 bag/ha",
            }),
            'description': forms.Textarea(attrs={
                'class': _TEXTAREA,
                'rows': 3,
                'placeholder': 'Detailed notes, dosage, observations…',
            }),
            'input_cost': forms.NumberInput(attrs={
                'class': _INPUT, 'step': '0.01',
                'placeholder': 'Material/input cost (PHP)',
            }),
            'labor_cost': forms.NumberInput(attrs={
                'class': _INPUT, 'step': '0.01',
                'placeholder': 'Labor cost (PHP)',
            }),
            'problem_observed': forms.TextInput(attrs={
                'class': _INPUT,
                'placeholder': 'e.g. Brown spot on lower leaves',
            }),
            'problem_severity': forms.Select(attrs={
                'class': _SELECT,
            }),
            'action_taken': forms.Textarea(attrs={
                'class': _TEXTAREA,
                'rows': 2,
                'placeholder': 'What did you do to address it?',
            }),
            'detection_record': forms.Select(attrs={
                'class': _SELECT,
            }),
            'workers_count': forms.NumberInput(attrs={
                'class': _INPUT, 'min': 0,
                'placeholder': 'Number of workers',
            }),
        }
        labels = {
            'activity_date':    'Date',
            'activity_type':    'Activity Type',
            'title':            'Activity Summary',
            'description':      'Detailed Notes',
            'input_cost':       'Input/Material Cost (PHP)',
            'labor_cost':       'Labor Cost (PHP)',
            'problem_observed': 'Problem Observed',
            'problem_severity': 'Severity',
            'action_taken':     'Action Taken',
            'detection_record': 'Link to AI Scan (optional)',
            'workers_count':    'Workers / Laborers',
        }

    def __init__(self, *args, season_log=None, owner_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required  = False
        self.fields['input_cost'].required   = False
        self.fields['labor_cost'].required   = False
        self.fields['problem_observed'].required = False
        self.fields['action_taken'].required  = False
        self.fields['workers_count'].required = False

        # Filter detection records to those belonging to this season's field/owner
        if season_log:
            self.fields['detection_record'].queryset = DetectionRecord.objects.filter(
                planting__field=season_log.field, is_active=True
            ).order_by('-created_at')
        elif owner_profile:
            self.fields['detection_record'].queryset = DetectionRecord.objects.filter(
                user=owner_profile, is_active=True
            ).order_by('-created_at')
        else:
            self.fields['detection_record'].queryset = DetectionRecord.objects.none()
        self.fields['detection_record'].required = False
        self.fields['detection_record'].empty_label = "— No AI scan linked —"


class SiteSettingForm(forms.ModelForm):
    """
    Simple form para sa global system settings (web UI).

    Tagalog:
    - Ginagamit ng admin sa custom web page (hindi sa Django admin site)
      para i-set kung ilang araw pabalik ang pinapayagan na `planting_date`.
    """

    class Meta:
        from .models import SiteSetting

        model = SiteSetting
        fields = [
            "allowed_past_days_planting",
            "detection_confidence_threshold",
            "yield_cnn_enabled",
            "email_enabled",
        ]
        labels = {
            "allowed_past_days_planting": "Allowed Past Days for Planting Date",
            "detection_confidence_threshold": "AI Detection Confidence Threshold",
            "yield_cnn_enabled": "Enable CNN Yield Model",
            "email_enabled": "Enable Outgoing Emails",
        }
        help_texts = {
            "allowed_past_days_planting": (
                "How many days back users can set a planting date. "
                "For example, 30 means the planting date can be up to 30 days ago. "
                "0 means only today is allowed."
            ),
            "detection_confidence_threshold": (
                "Minimum confidence (%) required for the AI model to accept an image. "
                "If the model is less confident, it will return 'Unknown/Not Rice'."
            ),
            "yield_cnn_enabled": (
                "When enabled, users can select CNN Yield mode (requires canopy image). "
                "When disabled, only Linear Regression is available."
            ),
            "email_enabled": (
                "Enable all outgoing email notifications globally. "
                "SMTP credentials are still required via environment settings."
            ),
        }
        widgets = {
            "allowed_past_days_planting": forms.NumberInput(
                attrs={
                    "class": INPUT_CLASS,
                    "min": "0",
                    "step": "1",
                }
            ),
            "detection_confidence_threshold": forms.NumberInput(
                attrs={
                    "class": INPUT_CLASS,
                    "min": "0",
                    "max": "100",
                    "step": "1",
                }
            ),
            "yield_cnn_enabled": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded",
                }
            ),
            "email_enabled": forms.CheckboxInput(
                attrs={
                    "class": "h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded",
                }
            ),
        }
