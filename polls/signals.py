"""
Django signals for automatic Profile creation, farm size updates,
and real-time in-app notifications.

Best Practice for Production:
- Signals are in separate file for better organization
- Registered in apps.py to ensure they load
- Handles both superuser and regular user creation
- Auto-computes farm_size_ha from field totals
- Auto-creates Notification on disease detection and yield drop
"""

import logging

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone

# Cache previous model state between pre_save and post_save handlers so we can
# detect transitions (e.g. unpublished → published) without requiring extra
# DB fields or third-party trackers.
_PRE_SAVE_STATE_CACHE: dict[tuple[str, int], dict[str, bool]] = {}

logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create Profile when User is created.
    
    Rules:
    - Superusers (is_superuser=True) → 'admin' role
    - Staff users (is_staff=True) → 'admin' role  
    - Regular users → 'farmer' role (default)
    
    This ensures:
    - python manage.py createsuperuser → auto creates admin profile
    - User registration → auto creates farmer profile
    - Admin creates user via web → auto creates profile with chosen role
    """
    if created:
        from .models import Profile
        
        # Determine role based on user permissions
        if instance.is_superuser or instance.is_staff:
            role = 'admin'
            location = 'Main Office'
        else:
            role = 'farmer'
            location = ''
        
        # Create profile if it doesn't exist
        Profile.objects.get_or_create(
            user=instance,
            defaults={
                'role': role,
                'location': location
            }
        )


@receiver(post_save, sender='polls.Field')
def update_farm_size_on_field_save(sender, instance, **kwargs):
    """
    BEST PRACTICE: Auto-update farm_size_ha when a field is created or updated.
    
    Triggers when:
    - New field is created
    - Existing field area is changed
    - Field owner is changed
    """
    if instance.owner:
        instance.owner.update_farm_size()


@receiver(post_delete, sender='polls.Field')
def update_farm_size_on_field_delete(sender, instance, **kwargs):
    """
    BEST PRACTICE: Auto-update farm_size_ha when a field is deleted.
    
    Ensures farm_size stays accurate even when fields are removed.
    """
    if instance.owner:
        instance.owner.update_farm_size()


# ============================================================================
# REAL-TIME NOTIFICATION SIGNALS
# ============================================================================

def _active_staff_profiles():
    """Return active admin and technician profiles for staff-facing alerts."""
    from .models import Profile

    return (
        Profile.objects
        .select_related('user')
        .filter(role__in=['admin', 'technician'], user__is_active=True)
    )


def _create_staff_notifications(
    *,
    alert_type,
    title,
    message,
    related_detection=None,
    related_yield=None,
    exclude_profile_ids=None,
    send_email=False,
):
    """Create in-app notifications for every active admin and technician.

    Staff notifications reuse the same related detection or yield record as the
    farmer alert so the notifications page can link directly to the record for
    review. Profiles listed in ``exclude_profile_ids`` are skipped to avoid
    sending the same event twice to one user.

    Returns:
        list: Created Notification rows.
    """
    from .models import Notification
    from . import services as _svc

    staff_profiles = _active_staff_profiles()
    excluded_ids = {pk for pk in (exclude_profile_ids or []) if pk}
    if excluded_ids:
        staff_profiles = staff_profiles.exclude(pk__in=excluded_ids)

    created_notifications = []
    for staff in staff_profiles:
        notification = Notification.objects.create(
            recipient=staff,
            type=alert_type,
            title=title,
            message=message,
            related_detection=related_detection,
            related_yield=related_yield,
        )
        created_notifications.append(notification)
        if send_email and staff.user.email:
            _svc.schedule_notification_email_send(notification.pk)

    return created_notifications


@receiver(post_save, sender='polls.DetectionRecord')
def notify_disease_detected(sender, instance, created, **kwargs):
    """
    Auto-create in-app Notifications when a disease is detected.

    Recipients:
    - The field owner (farmer) receives the actionable alert.
    - All active admins and technicians receive a review alert for every
      non-healthy detection, not only critical ones.

    Critical detections (70% severity or higher) also send an immediate staff
    email. Healthy scans and duplicate saves are ignored.
    """
    if not created:
        return

    try:
        from .models import Notification
        from . import services as _svc

        disease = instance.disease
        if not disease:
            return  # No disease recorded - skip

        disease_name = disease.name
        if 'healthy' in disease_name.lower():
            return  # Healthy scan - no alert needed

        # Prefer the field owner (farmer) as the actionable recipient.
        # Fall back to the scanner (technician/farmer) if no field owner is linked.
        recipient = None
        if instance.planting and instance.planting.field and instance.planting.field.owner:
            recipient = instance.planting.field.owner
        if not recipient:
            recipient = instance.user

        severity = instance.severity_pct or 0
        severity_label = "High" if severity >= 70 else "Moderate" if severity >= 40 else "Low"

        if recipient:
            notif = Notification.objects.create(
                recipient=recipient,
                type='disease',
                title=f'Disease Detected: {disease_name}',
                message=(
                    f'A scan on your field detected {disease_name} '
                    f'with {severity:.0f}% severity ({severity_label}). '
                    f'Immediate treatment is recommended. '
                    f'Check the scan record for detailed treatment advice.'
                ),
                related_detection=instance,
            )
            # Send email alert to the farmer (only if EMAIL_ENABLED=True in settings)
            _svc.schedule_notification_email_send(notif.pk)

        field = instance.planting.field if instance.planting else None
        field_name = field.name if field else 'Unknown Field'
        farmer_name = (
            (recipient.user.get_full_name() or recipient.user.username)
            if recipient else 'Unknown Farmer'
        )
        location_parts = [
            part for part in (
                field.barangay if field else '',
                field.municipality if field else '',
                field.province if field else '',
            ) if part
        ]
        location_text = f" ({', '.join(location_parts)})" if location_parts else ''

        # Every disease detection is visible to staff so they can review it.
        _create_staff_notifications(
            alert_type='disease',
            title=f'Disease Detected: {disease_name} ({severity:.0f}% severity)',
            message=(
                f'A scan on {farmer_name}\'s field "{field_name}"{location_text} '
                f'detected {disease_name} with {severity:.0f}% severity ({severity_label}). '
                f'Please review the detection record and follow up with the farmer.'
            ),
            related_detection=instance,
            exclude_profile_ids=[recipient.pk] if recipient else [],
        )

        # Critical detections also trigger an immediate staff email.
        if severity >= 70:
            from .models import Profile

            staff_profiles = Profile.objects.select_related('user').filter(
                role__in=['admin', 'technician'],
                user__is_active=True,
            ).exclude(user__email='')
            if recipient:
                staff_profiles = staff_profiles.exclude(pk=recipient.pk)

            for staff in staff_profiles:
                _svc.send_plain_email(
                    recipient_email=staff.user.email,
                    subject=f'[CRITICAL ALERT] {disease_name} - {severity:.0f}% Severity',
                    body=(
                        f"Hello {staff.user.get_full_name() or staff.user.username},\n\n"
                        f"A CRITICAL disease detection requires your attention.\n\n"
                        f"Disease  : {disease_name}\n"
                        f"Severity : {severity:.0f}% ({severity_label})\n"
                        f"Farmer   : {farmer_name}\n"
                        f"Field    : {field_name}{location_text}\n\n"
                        f"Please review and follow up with the farmer immediately.\n"
                        f"View detection records: {_svc._app_url('/detections/')}\n\n"
                        f"---\nAgriScan+ System"
                    ),
                )

    except Exception:
        logger.exception("Failed to create disease notification for DetectionRecord pk=%s", instance.pk)


@receiver(post_save, sender='polls.YieldPrediction')
def notify_yield_drop(sender, instance, created, **kwargs):
    """
    Auto-create in-app Notifications when a significant yield drop is predicted.

    Recipients:
    - The planting owner (farmer) receives the actionable alert.
    - All active admins and technicians receive a review alert so they can
      validate the prediction and follow up with the farmer.

    Threshold: at least 20% below the historical average, or below 2.0 tons/ha
    when no historical baseline exists.
    """
    if not created:
        return

    try:
        from .models import Notification
        from . import services as _svc

        # Determine recipient - prefer the planting owner, else the detection user.
        recipient = None
        if instance.planting and instance.planting.field and instance.planting.field.owner:
            recipient = instance.planting.field.owner
        elif instance.detection and instance.detection.user:
            recipient = instance.detection.user

        # Only alert on meaningful yield drop vs historical baseline.
        predicted = instance.predicted_yield_tons_per_ha
        if not predicted:
            return

        historical = None
        if instance.planting:
            from .services import get_historical_yield_data
            hist = get_historical_yield_data(instance.planting)
            if hist.get('record_count', 0) > 0:
                historical = hist.get('historical_yield')

        predicted_f = float(predicted)

        if historical:
            historical_f = float(historical)
            if historical_f <= 0:
                return

            drop_pct = (historical_f - predicted_f) / historical_f * 100

            if drop_pct < 20:
                return  # Less than 20% drop - no alert needed

            title = f'Yield Drop Alert: {drop_pct:.0f}% Below Historical'
            message = (
                f'Your predicted yield is {predicted_f:.2f} tons/ha, '
                f'which is {drop_pct:.0f}% lower than your historical average '
                f'of {historical_f:.2f} tons/ha. '
                f'This may be due to disease impact or unfavorable conditions. '
                f'Consider consulting a DA technician for advice.'
            )
            staff_summary = (
                f'{drop_pct:.0f}% below the historical average of '
                f'{historical_f:.2f} tons/ha'
            )
        else:
            # No historical baseline - alert if yield is critically low (<2 tons/ha).
            LOW_YIELD_THRESHOLD = 2.0
            if predicted_f >= LOW_YIELD_THRESHOLD:
                return

            title = f'Low Yield Prediction: {predicted_f:.2f} tons/ha'
            message = (
                f'Your predicted yield of {predicted_f:.2f} tons/ha is critically low '
                f'(below {LOW_YIELD_THRESHOLD} tons/ha). '
                f'No historical baseline is available for your planting record. '
                f'Please consult a DA technician for guidance.'
            )
            staff_summary = (
                f'critically low (below {LOW_YIELD_THRESHOLD} tons/ha) with no '
                f'historical baseline'
            )

        if recipient:
            notif = Notification.objects.create(
                recipient=recipient,
                type='yield_drop',
                title=title,
                message=message,
                related_yield=instance,
            )
            _svc.schedule_notification_email_send(notif.pk)

        field = None
        if instance.planting:
            field = instance.planting.field
        elif instance.detection and instance.detection.planting:
            field = instance.detection.planting.field
        field_name = field.name if field else 'Unknown Field'
        farmer_name = (
            (recipient.user.get_full_name() or recipient.user.username)
            if recipient else 'Unknown Farmer'
        )

        # Send the same alert to admins and technicians so they can review it.
        _create_staff_notifications(
            alert_type='yield_drop',
            title=title,
            message=(
                f'A yield prediction for {farmer_name}\'s field "{field_name}" '
                f'is {staff_summary}. Predicted yield: {predicted_f:.2f} tons/ha. '
                f'Please review the yield record and follow up with the farmer.'
            ),
            related_yield=instance,
            exclude_profile_ids=[recipient.pk] if recipient else [],
            send_email=True,
        )

    except Exception:
        logger.exception("Failed to create yield drop notification for YieldPrediction pk=%s", instance.pk)


@receiver(post_save, sender='polls.Announcement')
def notify_new_announcement(sender, instance, created, **kwargs):
    """
    Auto-create in-app Notifications only when an announcement is newly
    published:
    - created=True and is_active=True and not deleted
    - created=False and transition draft -> active (not deleted)

    Important: do NOT send during archive/restore/edit-only saves.
    """
    # Ignore archived announcements entirely.
    if instance.is_deleted:
        return

    # Created: notify only if immediately published.
    if created:
        if not instance.is_active:
            return
    else:
        # Update path: notify only on draft -> active transition.
        prev = _PRE_SAVE_STATE_CACHE.pop(('announcement', instance.pk), None)
        if not prev:
            return
        if prev.get('is_deleted'):
            return
        became_active = (not prev.get('is_active')) and instance.is_active
        if not became_active:
            return

    # Scheduled future announcements are dispatched by due-time jobs.
    if instance.published_at and instance.published_at > timezone.now():
        return

    try:
        from .models import Notification, Profile
        from django.db.models import Q

        # Resolve target profiles (same logic as get_target_users)
        audience = instance.target_audience
        if audience == 'all':
            target_profiles = Profile.objects.filter(user__is_active=True).select_related('user')
        elif audience == 'farmers':
            target_profiles = Profile.objects.filter(role='farmer', user__is_active=True).select_related('user')
        elif audience == 'technicians':
            target_profiles = Profile.objects.filter(role='technician', user__is_active=True).select_related('user')
        elif audience == 'barangay' and instance.target_barangay:
            target_profiles = Profile.objects.filter(
                role='farmer', user__is_active=True,
                fields__barangay__iexact=instance.target_barangay,
            ).distinct().select_related('user')
        elif audience == 'user' and instance.target_user_id:
            target_profiles = Profile.objects.filter(pk=instance.target_user_id).select_related('user')
        else:
            return

        # Build bell notifications (bulk_create, ignore duplicates)
        notifs = [
            Notification(
                recipient=profile,
                type='advisory',
                title=f'New Announcement: {instance.title}',
                message=(
                    f'{instance.content[:200]}{"..." if len(instance.content) > 200 else ""}'
                ),
                related_announcement=instance,
            )
            for profile in target_profiles
        ]
        if notifs:
            Notification.objects.bulk_create(notifs, ignore_conflicts=True)

    except Exception:
        logger.exception(
            "Failed to create announcement notifications for Announcement pk=%s", instance.pk
        )


@receiver(pre_save, sender='polls.Announcement')
def _cache_prev_announcement_state(sender, instance, **kwargs):
    """Cache previous announcement publish/archive flags for transition checks."""
    if not instance.pk:
        return
    try:
        old = sender.objects.only('is_active', 'is_deleted').get(pk=instance.pk)
        _PRE_SAVE_STATE_CACHE[('announcement', instance.pk)] = {
            'is_active': old.is_active,
            'is_deleted': old.is_deleted,
        }
    except sender.DoesNotExist:
        pass


# ---------------------------------------------------------------------------
# Knowledge / Treatment / Settings Notifications
# ---------------------------------------------------------------------------

@receiver(pre_save, sender='polls.KnowledgeBaseEntry')
def _cache_prev_knowledge_state(sender, instance, **kwargs):
    """Cache a small slice of previous state so we can detect a publish transition."""
    if not instance.pk:
        return
    try:
        old = sender.objects.only('is_published', 'is_active').get(pk=instance.pk)
        _PRE_SAVE_STATE_CACHE[('knowledge', instance.pk)] = {
            'is_published': old.is_published,
            'is_active': old.is_active,
        }
    except sender.DoesNotExist:
        pass


@receiver(post_save, sender='polls.KnowledgeBaseEntry')
def notify_new_knowledge_entry(sender, instance, created, **kwargs):
    """Notify farmers when new knowledge entries are published."""
    prev = _PRE_SAVE_STATE_CACHE.pop(('knowledge', instance.pk), None)

    # Notify only when the entry is active and published.
    if not instance.is_active or not instance.is_published:
        return

    should_notify = False
    if created:
        should_notify = True
    elif prev and not prev.get('is_published', False):
        should_notify = True

    if not should_notify:
        return

    try:
        from .models import Notification, Profile

        title = f"New Knowledge Entry: {instance.name}"
        message = (
            f"A new knowledge base entry has been published: {instance.name}.\n\n"
            f"{(instance.description or '').strip()[:250]}"  # include a short preview
        )

        profiles = Profile.objects.filter(role='farmer', user__is_active=True).select_related('user')
        notifs = [
            Notification(
                recipient=profile,
                type='knowledge',
                title=title,
                message=message,
                related_knowledge=instance,
            )
            for profile in profiles
        ]

        if notifs:
            from . import services as _svc
            created_notifs = [
                Notification.objects.create(
                    recipient=notification.recipient,
                    type=notification.type,
                    title=notification.title,
                    message=notification.message,
                    related_detection=notification.related_detection,
                    related_yield=notification.related_yield,
                    related_announcement=notification.related_announcement,
                    related_knowledge=notification.related_knowledge,
                    related_treatment=notification.related_treatment,
                    related_site_setting_audit=notification.related_site_setting_audit,
                )
                for notification in notifs
            ]
            for notification in created_notifs:
                _svc.schedule_notification_email_send(notification.pk)

    except Exception:
        logger.exception(
            "Failed to create knowledge notifications for entry pk=%s", instance.pk
        )


@receiver(pre_save, sender='polls.TreatmentRecommendation')
def _cache_prev_treatment_state(sender, instance, **kwargs):
    """Cache a small slice of previous state so we can detect activation."""
    if not instance.pk:
        return
    try:
        old = sender.objects.only('is_active').get(pk=instance.pk)
        _PRE_SAVE_STATE_CACHE[('treatment', instance.pk)] = {
            'is_active': old.is_active,
        }
    except sender.DoesNotExist:
        pass


@receiver(post_save, sender='polls.TreatmentRecommendation')
def notify_new_treatment(sender, instance, created, **kwargs):
    """Notify staff when new treatment recommendations are added/activated."""
    prev = _PRE_SAVE_STATE_CACHE.pop(('treatment', instance.pk), None)

    # Notify only when the treatment is active.
    if not instance.is_active:
        return

    should_notify = False
    if created:
        should_notify = True
    elif prev and not prev.get('is_active', False):
        should_notify = True

    if not should_notify:
        return

    try:
        from .models import Notification, Profile

        title = f"New Treatment Recommendation: {instance.disease.name}"
        message = (
            f"A new treatment recommendation has been published for {instance.disease.name}.\n\n"
            f"{(instance.short_text or '').strip()}"
        )

        profiles = Profile.objects.filter(role__in=['admin', 'technician'], user__is_active=True).select_related('user')
        notifs = [
            Notification(
                recipient=profile,
                type='treatment',
                title=title,
                message=message,
                related_treatment=instance,
            )
            for profile in profiles
        ]

        if notifs:
            from . import services as _svc
            created_notifs = [
                Notification.objects.create(
                    recipient=notification.recipient,
                    type=notification.type,
                    title=notification.title,
                    message=notification.message,
                    related_detection=notification.related_detection,
                    related_yield=notification.related_yield,
                    related_announcement=notification.related_announcement,
                    related_knowledge=notification.related_knowledge,
                    related_treatment=notification.related_treatment,
                    related_site_setting_audit=notification.related_site_setting_audit,
                )
                for notification in notifs
            ]
            for notification in created_notifs:
                _svc.schedule_notification_email_send(notification.pk)

    except Exception:
        logger.exception(
            "Failed to create treatment notifications for TreatmentRecommendation pk=%s", instance.pk
        )


@receiver(post_save, sender='polls.SiteSettingAudit')
def notify_system_setting_changes(sender, instance, created, **kwargs):
    """Notify all active users when system settings are updated."""
    if not created:
        return

    try:
        from .models import Notification, Profile, SiteSetting

        changed_by = instance.changed_by
        who = (changed_by.get_full_name() or changed_by.username) if changed_by else "System"
        title = "System Settings Updated"

        details = instance.details or {}
        changes = details.get('changes') or {}

        # Ignore no-op changes where values did not actually differ.
        filtered_changes = {}
        for key, diff in changes.items():
            if not isinstance(diff, dict):
                continue
            from_value = diff.get('from')
            to_value = diff.get('to')
            if from_value == to_value:
                continue
            filtered_changes[key] = diff

        change_lines = []
        for key, diff in filtered_changes.items():
            # Use the field verbose_name when available for better readability.
            label = key
            try:
                field = SiteSetting._meta.get_field(key)
                label = getattr(field, 'verbose_name', key)
            except Exception:
                pass

            from_value = diff.get('from')
            to_value = diff.get('to')
            change_lines.append(f"- {label}: {from_value} → {to_value}")

        change_summary = "\n".join(change_lines) if change_lines else "(no changes detected)"

        message = (
            f"{who} updated system settings.\n\n"
            f"Changes:\n{change_summary}\n\n"
            f"Note: These are global settings that affect how AgriScan behaves for all users."
        )

        profiles = Profile.objects.filter(user__is_active=True).select_related('user')
        notifs = [
            Notification(
                recipient=profile,
                type='system',
                title=title,
                message=message,
                related_site_setting_audit=instance,
            )
            for profile in profiles
        ]

        if notifs:
            from django.db import transaction
            from . import services as _svc
            created_notifs = [
                Notification.objects.create(
                    recipient=notification.recipient,
                    type=notification.type,
                    title=notification.title,
                    message=notification.message,
                    related_detection=notification.related_detection,
                    related_yield=notification.related_yield,
                    related_announcement=notification.related_announcement,
                    related_knowledge=notification.related_knowledge,
                    related_treatment=notification.related_treatment,
                    related_site_setting_audit=notification.related_site_setting_audit,
                )
                for notification in notifs
            ]

            notification_ids = [
                notification.pk
                for notification in created_notifs
                if notification.pk
            ]
            def queue_emails() -> None:
                for notification_id in notification_ids:
                    _svc.queue_notification_email_send(notification_id)

            transaction.on_commit(queue_emails)

    except Exception:
        logger.exception(
            "Failed to create system setting notifications for SiteSettingAudit pk=%s", instance.pk
        )
