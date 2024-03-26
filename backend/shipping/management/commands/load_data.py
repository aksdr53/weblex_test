import csv

from django.core.management.base import BaseCommand

from shipping.models import Location
from backend.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(BASE_DIR / 'uszips.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            locations = []
            for row in reader:
                locations.append(Location(
                    city=row['city'],
                    state=row['state_name'],
                    zip_code=row['zip'],
                    latitude=row['lat'],
                    longitude=row['lng']
                ))
        Location.objects.bulk_create(locations)