from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0022_remove_seasonlog_current_stage"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="onboarding_guide_dismissed",
            field=models.BooleanField(
                default=False,
                help_text="Do not show the welcome guide modal after sign-in.",
            ),
        ),
    ]
