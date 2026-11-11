from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("polls", "0016_alter_harvestrecord_planting"),
    ]

    operations = [
        migrations.DeleteModel(
            name="FarmActivity",
        ),
        migrations.CreateModel(
            name="CropStatusCheckIn",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("healthy", "Healthy"),
                            ("needs_attention", "Needs attention"),
                            ("ready_to_harvest", "Ready to harvest"),
                            ("harvested", "Harvested"),
                        ],
                        max_length=24,
                    ),
                ),
                (
                    "issue",
                    models.CharField(
                        choices=[
                            ("none", "No problem"),
                            ("pest", "Pest"),
                            ("disease", "Disease"),
                            ("water", "Water problem"),
                            ("nutrient", "Nutrient problem"),
                            ("other", "Other"),
                        ],
                        default="none",
                        max_length=20,
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                (
                    "planting",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="crop_checkins",
                        to="polls.plantingrecord",
                    ),
                ),
                (
                    "season_log",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="checkins",
                        to="polls.seasonlog",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(
                        fields=["season_log", "-created_at"],
                        name="polls_cropst_season__c8fbb5_idx",
                    ),
                    models.Index(
                        fields=["planting", "-created_at"],
                        name="polls_cropst_planting_1dfc13_idx",
                    ),
                ],
            },
        ),
    ]
