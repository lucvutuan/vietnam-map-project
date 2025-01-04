def read_coordinates(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                lat, lon = map(float, line.strip().split(','))
                coordinates.append((lat, lon))
            except ValueError:
                continue  # Skip lines that do not contain valid coordinates
    return coordinates

def validate_coordinates(coordinates):
    valid_coords = []
    for lat, lon in coordinates:
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            valid_coords.append((lat, lon))
    return valid_coords