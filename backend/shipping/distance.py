from geopy.distance import geodesic

def calculate_distance(truck_location, cargo_pickup_location):
    truck_coordinates = (truck_location[0], truck_location[1])
    cargo_pickup_coordinates = (cargo_pickup_location[0], cargo_pickup_location[1])
    distance = geodesic(truck_coordinates, cargo_pickup_coordinates).miles
    return distance