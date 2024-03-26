from .models import Location

def get_location_from_zip_code(zip_code):
    try:
        location = Location.objects.get(zip_code=zip_code)
        return location
    except Location.DoesNotExist:
        return None
