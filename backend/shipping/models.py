import random
import string

from django.core.exceptions import ValidationError
from django.db import models

#from .utils import get_location_from_zip_code


def validate_truck_number(value):
    if not (1000 <= int(value[:-1]) <= 9999 and value[-1] in string.ascii_uppercase):
        raise ValidationError(
            f"{value} is not a valid truck number. It should be a number between 1000 and 9999 followed by a capital letter."
        )


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.city}, {self.state} {self.zip_code}"


class Truck(models.Model):
    truck_number = models.CharField(max_length=5,
                                    unique=True,
                                    validators=[validate_truck_number])
    current_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    capacity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.truck_number
    
    @staticmethod
    def generate_unique_truck_number():
        number = random.randint(1000, 9999)
        letter = random.choice(string.ascii_uppercase)
        return f"{number}{letter}"
    

    def update_location_from_zip_code(self, zip_code):
        location = get_location_from_zip_code(zip_code)
        if location:
            self.current_location = location
            self.save()
            return True
        return False


class Cargo(models.Model):
    pick_up_location = models.ForeignKey(Location, related_name='pick_up_cargo', on_delete=models.CASCADE)
    delivery_location = models.ForeignKey(Location, related_name='delivery_cargo', on_delete=models.CASCADE)
    weight = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f"Cargo ID: {self.pk}"


def get_location_from_zip_code(zip_code):
    try:
        location = Location.objects.get(zip_code=zip_code)
        return location
    except Location.DoesNotExist:
        return None