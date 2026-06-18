from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0005_knowledgebaseentry_deleted_at_seasonlog_deleted_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesetting",
            name="yield_cnn_enabled",
            field=models.BooleanField(
                default=False,
                help_text=(
                    "Enable or disable CNN yield prediction in the user-facing Yield Tool. "
                    "When disabled, only Linear Regression is selectable."
                ),
            ),
        ),
    ]
