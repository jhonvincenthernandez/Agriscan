from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0008_announcement_deleted_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="harvestrecord",
            name="grain_quality",
            field=models.CharField(
                blank=True,
                help_text="Free-text grain quality (from variety or manual notes).",
                max_length=100,
                null=True,
            ),
        ),
    ]
