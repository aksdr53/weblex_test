import random

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Truck, Location

@receiver(post_save, sender=Truck)
def assign_random_location(sender, instance, created, **kwargs):
    if created:  # Проверяем, что машина была создана, а не обновлена
        all_locations = Location.objects.all()
        random_location = random.choice(all_locations)
        instance.current_location = random_location
        instance.save()