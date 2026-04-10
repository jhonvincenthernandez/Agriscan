from django.db import migrations, models
from django.utils import timezone


def backfill_announcement_deleted_at(apps, schema_editor):
    Announcement = apps.get_model('polls', 'Announcement')
    now = timezone.now()
    Announcement.objects.filter(is_deleted=True, deleted_at__isnull=True).update(deleted_at=now)


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_sitesetting_email_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='deleted_at',
            field=models.DateTimeField(
                blank=True,
                db_index=True,
                help_text='Timestamp when announcement was archived',
                null=True,
            ),
        ),
        migrations.RunPython(
            backfill_announcement_deleted_at,
            migrations.RunPython.noop,
        ),
    ]
