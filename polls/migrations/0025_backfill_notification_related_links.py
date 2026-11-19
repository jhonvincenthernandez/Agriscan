from bisect import bisect_right
from datetime import timedelta

from django.db import migrations


SYSTEM_MATCH_WINDOW = timedelta(minutes=15)
TREATMENT_TITLE_PREFIX = "New Treatment Recommendation: "
TREATMENT_MESSAGE_PREFIX = (
    "A new treatment recommendation has been published for {disease}.\n\n"
)


def backfill_related_links(apps, schema_editor):
    """Attach existing treatment and system alerts to their source records."""
    Notification = apps.get_model("polls", "Notification")
    SiteSettingAudit = apps.get_model("polls", "SiteSettingAudit")
    TreatmentRecommendation = apps.get_model("polls", "TreatmentRecommendation")

    # System notifications are created immediately after their audit entry.
    # Match each notification to the closest earlier active audit.
    audits = list(
        SiteSettingAudit.objects.filter(is_active=True)
        .order_by("changed_at")
        .values_list("pk", "changed_at")
    )
    audit_times = [changed_at for _, changed_at in audits]
    system_updates = []

    system_notifications = (
        Notification.objects.filter(
            type="system",
            related_site_setting_audit__isnull=True,
        )
        .only("pk", "created_at")
        .order_by("created_at")
    )
    for notification in system_notifications.iterator():
        index = bisect_right(audit_times, notification.created_at) - 1
        if index < 0:
            continue

        audit_pk, changed_at = audits[index]
        if notification.created_at - changed_at > SYSTEM_MATCH_WINDOW:
            continue

        system_updates.append((notification.pk, audit_pk))

    for notification_pk, audit_pk in system_updates:
        Notification.objects.filter(pk=notification_pk).update(
            related_site_setting_audit_id=audit_pk
        )

    # Treatment notifications include the disease and the short recommendation.
    # Use both values to identify the exact treatment that was published.
    treatment_notifications = (
        Notification.objects.filter(
            type="treatment",
            related_treatment__isnull=True,
        )
        .only("pk", "title", "message", "created_at")
        .order_by("created_at")
    )
    for notification in treatment_notifications.iterator():
        if not notification.title.startswith(TREATMENT_TITLE_PREFIX):
            continue

        disease_name = notification.title[len(TREATMENT_TITLE_PREFIX):].strip()
        message = notification.message or ""
        message_prefix = TREATMENT_MESSAGE_PREFIX.format(disease=disease_name)
        short_text = ""
        if message.startswith(message_prefix):
            short_text = message[len(message_prefix):].strip()

        candidates = TreatmentRecommendation.objects.filter(
            disease__name=disease_name,
        )
        if short_text:
            candidates = candidates.filter(short_text=short_text)

        match = (
            candidates.filter(
                created_at__lte=notification.created_at + timedelta(seconds=5),
            )
            .order_by("-created_at")
            .first()
        )
        if match is None:
            match = candidates.order_by("-created_at").first()

        if match is not None:
            Notification.objects.filter(pk=notification.pk).update(
                related_treatment_id=match.pk
            )


def reverse_backfill(apps, schema_editor):
    """No-op: the original records did not store these links."""


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0024_notification_related_site_setting_audit_and_more"),
    ]

    operations = [
        migrations.RunPython(backfill_related_links, reverse_backfill),
    ]
