from django.core.management.base import BaseCommand
from ticket.models import ScenicSpot

class Command(BaseCommand):
    help = 'Check scenic spot tags after cleaning'

    def handle(self, *args, **options):
        self.stdout.write('Checking scenic spot tags after cleaning:')
        scenic_spots = ScenicSpot.objects.all()
        for spot in scenic_spots:
            self.stdout.write(f'{spot.name}: {spot.tags}')
        self.stdout.write(f'Total scenic spots: {scenic_spots.count()}')
