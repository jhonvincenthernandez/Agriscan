from datetime import timedelta

from django.db import migrations


KNOWLEDGE_TITLE_PREFIX = "New Knowledge Entry: "


def backfill_related_knowledge(apps, schema_editor):
    """Attach existing knowledge alerts to their source entries."""
    Notification = apps.get_model("polls", "Notification")
    KnowledgeBaseEntry = apps.get_model("polls", "KnowledgeBaseEntry")

    notifications = (
        Notification.objects.filter(
            type="knowledge",
            related_knowledge__isnull=True,
        )
        .only("pk", "title", "created_at")
        .order_by("created_at")
    )

    for notification in notifications.iterator():
        if not notification.title.startswith(KNOWLEDGE_TITLE_PREFIX):
            continue

        entry_name = notification.title[len(KNOWLEDGE_TITLE_PREFIX):].strip()
        match = (
            KnowledgeBaseEntry.objects.filter(
                name=entry_name,
                created_at__lte=notification.created_at + timedelta(seconds=5),
            )
            .order_by("-created_at")
            .first()
        )

        if match is not None:
            Notification.objects.filter(pk=notification.pk).update(
                related_knowledge_id=match.pk
            )


def reverse_backfill(apps, schema_editor):
    """No-op: the original records did not store this link."""


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0026_notification_related_knowledge"),
    ]

    operations = [
        migrations.RunPython(backfill_related_knowledge, reverse_backfill),
    ]
