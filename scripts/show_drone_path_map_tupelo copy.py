import folium
import random
import math
import time
from folium.elements import Element

def generate_new_point(initial_lat, initial_lon, distance_km, bearing_deg):
    """
    Generates a new latitude and longitude given a starting point, 
    distance, and bearing.

    :param initial_lat: Starting latitude in degrees.
    :param initial_lon: Starting longitude in degrees.
    :param distance_km: Distance to travel in kilometers.
    :param bearing_deg: Bearing (direction) in degrees, clockwise from North.
    :return: A tuple (new_lat, new_lon) in degrees.
    """
    # Earth's radius in kilometers
    R = 6378.1 #

    # Convert degrees to radians
    lat1 = math.radians(initial_lat)
    lon1 = math.radians(initial_lon)
    bearing_rad = math.radians(bearing_deg)
    
    # Angular distance
    angular_distance = distance_km / R

    # Calculate new latitude
    lat2 = math.asin(math.sin(lat1) * math.cos(angular_distance) +
                    math.cos(lat1) * math.sin(angular_distance) * math.cos(bearing_rad))
    
    # Calculate new longitude
    lon2 = lon1 + math.atan2(math.sin(bearing_rad) * math.sin(angular_distance) * math.cos(lat1),
                             math.cos(angular_distance) - math.sin(lat1) * math.sin(lat2))
    
    # Convert radians back to degrees
    new_lat = math.degrees(lat2)
    new_lon = math.degrees(lon2)
    
    return (new_lat, new_lon)


line1_coordinates = [
]

inv_coordinates = [
]

# tupelo 30.148214, -95.530372
start_lat = 30.148214
start_lon = -95.530372

distance = 0.0025       # Distance in km

latitude = start_lat
longitude = start_lon
bearing = 0

invasive_count = 0 

for a in range(1,100):    
    if a % 25 == 0:
        bearing += 90

    new_coordinates = generate_new_point(latitude, longitude, distance, bearing)
    latitude = new_coordinates[0]
    longitude = new_coordinates[1]
    line1_coordinates.append([latitude, longitude])

    random_boolean = random.randint(0, 1) == 1
    if random_boolean and invasive_count < 11:        
        if a <= 25:
            new_coordinates = generate_new_point(latitude, longitude, -0.01, 60)
            invasive_count += 1
            inv_coordinates.append(new_coordinates)

        if a > 25 and a <= 50:
            new_coordinates = generate_new_point(latitude, longitude, -0.02, 180)
            invasive_count += 1
            inv_coordinates.append(new_coordinates)

        if a > 50 and a <= 75:
            new_coordinates = generate_new_point(latitude, longitude, -0.03, 180)
            invasive_count += 1
            inv_coordinates.append(new_coordinates)

        if a > 75 and a <= 100:
            new_coordinates = generate_new_point(latitude, longitude, -0.04, 90)
            invasive_count += 1
            inv_coordinates.append(new_coordinates)

    # Create a map centered at a specific location
    m = folium.Map(location=[start_lat, start_lon], zoom_start=19)

    # Add a marker to the map
    line1 = folium.PolyLine(locations=line1_coordinates, color='blue', weight=5, opacity=0.8)
    line1.add_to(m)

    # Add start and end markers
    folium.Marker(
        location=line1_coordinates[0],
        popup='Start',
        icon=folium.Icon(color='green', icon='play', prefix='fa')
    ).add_to(m)

    folium.Marker(
        location=line1_coordinates[-1],
        popup='End',
        icon=folium.Icon(color='red', icon='stop', prefix='fa')
    ).add_to(m)

    for x in inv_coordinates:
        inv_m = folium.Marker(location=x,popup="Chinese Privet (Sev 3)", tooltip="Chinese Privet").add_to(m)
    
    # Display the map
    m.save("C:\\Venky\\invasive_species_detection\\drone_path\\drone_path_tupelo.html")


# Now plot invasives 
