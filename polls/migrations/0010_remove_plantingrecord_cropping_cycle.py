from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0009_alter_harvestrecord_grain_quality"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="plantingrecord",
            name="cropping_cycle",
        ),
    ]
