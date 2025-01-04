import matplotlib.pyplot as plt
import os
from geopy.distance import geodesic

def read_coordinates(file_path):
    """
    Read coordinates from a file and return them as a list of tuples.
    Each line in the file should contain a latitude and longitude separated by a comma.
    """
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            lat, lon = map(float, line.strip().split(','))
            coordinates.append((lat, lon))
    return coordinates

def read_dms_coordinates(file_path):
    """
    Read DMS coordinates from a file and return them as a list of tuples in decimal degrees.
    Each line in the file should contain a latitude and longitude in DMS format.
    """
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            lat_dms, lon_dms = line.strip().split()
            lat_deg = int(lat_dms[:2])
            lat_min = int(lat_dms[2:4])
            lat_sec = int(lat_dms[4:6])
            lat_dir = lat_dms[6]
            
            lon_deg = int(lon_dms[:3])
            lon_min = int(lon_dms[3:5])
            lon_sec = int(lon_dms[5:7])
            lon_dir = lon_dms[7]
            
            lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
            lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)
            
            coordinates.append((lat, lon))
    return coordinates

def filter_coordinates(coordinates, point1, point2):
    """
    Filter out coordinates that lie under the line connecting point1 and point2.
    """
    filtered_coordinates = []
    for lat, lon in coordinates:
        # Calculate the y-value of the line at the given x (longitude)
        y_on_line = point1[1] + (point2[1] - point1[1]) * (lon - point1[0]) / (point2[0] - point1[0])
        if lat >= y_on_line:
            filtered_coordinates.append((lat, lon))
    return filtered_coordinates

def filter_lat_lon(coordinates):
    """
    Filter out coordinates with latitude less than 14.5 and longitude greater than 107.5.
    """
    return [(lat, lon) for lat, lon in coordinates if not (lat < 14.5 and lon > 107.5)]

def dms_to_decimal(degrees, minutes, seconds, direction):
    """
    Convert DMS (Degrees, Minutes, Seconds) to decimal degrees.
    """
    decimal = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def cbi_coordinate(ax):
    """
    Draw a circle with the specified details.
    """
    # Center of the circle
    center_lat_dms = "204856N"
    center_lon_dms = "1064328E"
    
    # Point on the circle (PHUTA)
    point_lat_dms = "205547N"
    point_lon_dms = "1062738E"
    
    # Convert center coordinates to decimal degrees
    center_lat_deg = int(center_lat_dms[:2])
    center_lat_min = int(center_lat_dms[2:4])
    center_lat_sec = int(center_lat_dms[4:6])
    center_lat_dir = center_lat_dms[6]
    
    center_lon_deg = int(center_lon_dms[:3])
    center_lon_min = int(center_lon_dms[3:5])
    center_lon_sec = int(center_lon_dms[5:7])
    center_lon_dir = center_lon_dms[7]
    
    center_lat = dms_to_decimal(center_lat_deg, center_lat_min, center_lat_sec, center_lat_dir)
    center_lon = dms_to_decimal(center_lon_deg, center_lon_min, center_lon_sec, center_lon_dir)
    
    # Convert point coordinates to decimal degrees
    point_lat_deg = int(point_lat_dms[:2])
    point_lat_min = int(point_lat_dms[2:4])
    point_lat_sec = int(point_lat_dms[4:6])
    point_lat_dir = point_lat_dms[6]
    
    point_lon_deg = int(point_lon_dms[:3])
    point_lon_min = int(point_lon_dms[3:5])
    point_lon_sec = int(point_lon_dms[5:7])
    point_lon_dir = point_lon_dms[7]
    
    point_lat = dms_to_decimal(point_lat_deg, point_lat_min, point_lat_sec, point_lat_dir)
    point_lon = dms_to_decimal(point_lon_deg, point_lon_min, point_lon_sec, point_lon_dir)
    
    # Calculate the radius of the circle in kilometers
    center = (center_lat, center_lon)
    point = (point_lat, point_lon)
    radius_km = geodesic(center, point).km
    
    # Convert radius to degrees (approximation)
    radius_deg = radius_km * (1 / 111)  # 1 degree is approximately 111 km
    
    # Draw the circle
    circle = plt.Circle((center_lon, center_lat), radius_deg, color='blue', fill=False, linestyle='--')
    ax.add_patch(circle)
    
    # Draw the center as a black dot
    ax.scatter([center_lon], [center_lat], color='black', s=5)
    
    # Add label for the center
    ax.text(center_lon, center_lat, "CBI", fontsize=8, ha='right', color='black')

def add_custom_points(ax):
    """
    Add custom points to the map.
    """
    custom_points = {
        "PHUTA": ("205547N", "1062738E"),
        "VIBAO": ("203918N", "1062947E"),
        "VANUC": ("203259N", "1064318E"),
        "LOCHA": ("203924N", "1065713E"),
        "DOKLA": ("210412N", "1064328E"),
        "GASSO": ("210511N", "1064506E"),
    }
    
    for name, (lat_dms, lon_dms) in custom_points.items():
        lat_deg = int(lat_dms[:2])
        lat_min = int(lat_dms[2:4])
        lat_sec = int(lat_dms[4:6])
        lat_dir = lat_dms[6]
        
        lon_deg = int(lon_dms[:3])
        lon_min = int(lon_dms[3:5])
        lon_sec = int(lon_dms[5:7])
        lon_dir = lon_dms[7]
        
        lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
        lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)
        
        # Plot the custom point
        ax.scatter([lon], [lat], color='black', s=5)
        
        # Add label for the custom point
        ax.text(lon, lat, name, fontsize=6, ha='right', color='black')

def test_zone(ax, file_path):
    """
    Draw a zone using coordinates from a .txt file.
    """
    coordinates = read_dms_coordinates(file_path)
    
    latitudes, longitudes = zip(*coordinates)
    
    # Plot the zone
    ax.plot(longitudes, latitudes, c='green', linestyle='-', linewidth=0.5, marker='.')
    
    # Fill the zone with a light green color
    ax.fill(longitudes, latitudes, 'lightgreen', alpha=0.3)

    # Add labels for each point
    for i, (lat, lon) in enumerate(coordinates, start=1):
        ax.text(lon, lat, str(i), fontsize=6, ha='right', color='blue')


def draw_map(coordinates, file_path):
    """
    Draw a map using the provided coordinates.
    The map will display the points and connect them with lines.
    """
    point1 = (107.5038888888889, 14.464166666666666)
    point2 = (112.0, 14.5)
    
    # Filter coordinates
    coordinates = filter_coordinates(coordinates, point1, point2)
    coordinates = filter_lat_lon(coordinates)
    
    latitudes, longitudes = zip(*coordinates)
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Set the background color to light green
    ax.set_facecolor('lightgreen')
    
    # Plot the points
    scatter = ax.scatter(longitudes, latitudes, c='blue', marker='o', s=0.5)
    
    # Connect the points with lines
    line, = ax.plot(longitudes, latitudes, c='black', linewidth=0.5)

    # Fill the area inside the points with light yellow color
    ax.fill(longitudes, latitudes, 'yellow', alpha=0.3)
    
    # Set the title and labels
    ax.set_title('VIỆT NAM VÔ ĐỊCH')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    
    # Enable grid
    ax.grid(True)

    # Draw the circle with the specified details
    cbi_coordinate(ax)

    # Add custom points
    add_custom_points(ax)

    # Draw the zone from the .txt file
    test_zone(ax, file_path)

    # Maximize the figure window
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()

    # Variables to store the initial position of the mouse and the axis limits
    press = None

    def on_press(event):
        """
        Store the initial position of the mouse and the axis limits when the left mouse button is pressed.
        """
        nonlocal press
        if event.button == 1:  # Left mouse button
            press = (event.xdata, event.ydata, ax.get_xlim(), ax.get_ylim())

    def on_release(event):
        """
        Reset the press variable when the left mouse button is released.
        """
        nonlocal press
        if event.button == 1:  # Left mouse button
            press = None

    def on_motion(event):
        """
        Move the map when the left mouse button is pressed and the mouse is moved.
        """
        if press is None or event.xdata is None or event.ydata is None:
            return
        xpress, ypress, xlim, ylim = press
        dx = xpress - event.xdata
        dy = ypress - event.ydata
        ax.set_xlim(xlim[0] + dx, xlim[1] + dx)
        ax.set_ylim(ylim[0] + dy, ylim[1] + dy)
        fig.canvas.draw_idle()

    def on_zoom(event):
        """
        Handle zooming in and out using the mouse wheel.
        """
        base_scale = 1.2
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()
        xdata = event.xdata
        ydata = event.ydata
        
        # Determine the scale factor based on the scroll direction
        if event.button == 'up':
            scale_factor = 1 / base_scale
        elif event.button == 'down':
            scale_factor = base_scale
        elif event.button == 3:  # Right mouse button for horizontal zoom
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
            fig.canvas.draw_idle()
            return
        else:
            scale_factor = 1
            print(event.button)
        
        # Calculate new limits
        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
        
        # Set new limits
        ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
        ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
        
        # Redraw the figure
        fig.canvas.draw_idle()

    # Connect the zoom and pan events
    fig.canvas.mpl_connect("scroll_event", on_zoom)
    fig.canvas.mpl_connect("button_press_event", on_press)
    fig.canvas.mpl_connect("button_release_event", on_release)
    fig.canvas.mpl_connect("motion_notify_event", on_motion)
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the path to the data file
    data_file = os.path.join(base_dir, '..', 'data', 'VIETNAM_COORDINATE.txt')
    test_zone_file_path = os.path.join(base_dir, '..', 'data', 'TEST_ZONE.txt')
    
    # Check if the files exist
    if not os.path.exists(data_file):
        print(f"Error: The file {data_file} does not exist.")
    elif not os.path.exists(test_zone_file_path):
        print(f"Error: The file {test_zone_file_path} does not exist.")
    else:
        # Read coordinates and draw the map
        coordinates = read_coordinates(data_file)
        draw_map(coordinates, test_zone_file_path)