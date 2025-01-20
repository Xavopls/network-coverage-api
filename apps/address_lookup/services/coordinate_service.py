from geopy.distance import geodesic

def find_closest_geopy(lat, lon, coordinates):

    target = (lat, lon)
    closest = min(coordinates, key=lambda coord: geodesic(target, (coord[0], coord[1])).meters)
    return closest
