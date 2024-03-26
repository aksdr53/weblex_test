from geopy.distance import geodesic

def calculate_distance(truck_location, cargo_pickup_location):
    truck_coordinates = (truck_location.latitude, truck_location.longitude)
    cargo_pickup_coordinates = (cargo_pickup_location.latitude, cargo_pickup_location.longitude)
    distance = geodesic(truck_coordinates, cargo_pickup_coordinates).miles
    return distance