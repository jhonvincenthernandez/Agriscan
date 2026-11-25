from django.core.management.base import BaseCommand

from polls.models import PlantingRecord


class Command(BaseCommand):
    help = (
        'Synchronize planting statuses from planting dates and active harvest '
        'records. Use this command from a daily scheduler.'
    )

    def handle(self, *args, **options):
        updated_count = PlantingRecord.sync_lifecycle_statuses()
        self.stdout.write(
            self.style.SUCCESS(
                f'Updated {updated_count} planting record(s).'
            )
        )
