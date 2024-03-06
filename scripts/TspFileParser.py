import os
import math

def parse_tsp_file(filename) -> tuple:
    """
    Parses a TSP file and extracts node coordinates, edge weight type, edge weight format, explicit distances, and dimension.

    Parameters:
    - filename: The name of the file to be parsed.

    Returns:
    - A tuple containing node coordinates (dict), edge weight type (str), edge weight format (str), explicit distances (list), and dimension (int).
    """
    with open(filename, 'r') as f:
        content = f.readlines()
    edge_weight_type, edge_weight_format = "", ""
    node_coords, explicit_distances = {}, []
    reading_section = None
    dimension = 0

    for line in content:
        if "EDGE_WEIGHT_TYPE" in line:
            edge_weight_type = line.split(":")[1].strip()
        elif "EDGE_WEIGHT_FORMAT" in line:
            edge_weight_format = line.split(":")[1].strip()
        elif "DIMENSION" in line:
            dimension = int(line.split(":")[1].strip())
        elif line.strip() == "NODE_COORD_SECTION":
            reading_section = "NODE_COORD"
        elif line.strip() == "EDGE_WEIGHT_SECTION":
            reading_section = "EDGE_WEIGHT"
        elif line.strip() == "EOF":
            break
        elif reading_section == "NODE_COORD" and edge_weight_type != "EXPLICIT":
            parts = line.strip().split()
            if len(parts) == 3:
                try:
                    node_id, x, y = int(parts[0]), float(parts[1]), float(parts[2])
                    node_coords[node_id] = (x, y)
                except ValueError:
                    print(f"Skipping invalid line: {line.strip()}")
        elif reading_section == "EDGE_WEIGHT" and edge_weight_type == "EXPLICIT":
            try:
                explicit_distances.extend(map(float, line.strip().split()))
            except ValueError:
                print(f"Skipping invalid line: {line.strip()}")
    return node_coords, edge_weight_type, edge_weight_format, explicit_distances, dimension

def euclidean_distance(x1, y1, x2, y2) -> int:
    """
    Calculates the Euclidean distance between two points in 2D space.

    Parameters:
    - x1, y1: Coordinates of the first point.
    - x2, y2: Coordinates of the second point.

    Returns:
    - The rounded Euclidean distance between the two points.
    """
    return round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))

def geo_distance(deg_lat1, deg_lon1, deg_lat2, deg_lon2) -> int:
    """
    Calculate geographical distance using the Haversine formula on coordinates specified in degrees.

    Parameters:
    - deg_lat1, deg_lon1: Latitude and Longitude of point 1 in degrees.
    - deg_lat2, deg_lon2: Latitude and Longitude of point 2 in degrees.

    Returns:
    - Distance in kilometers.
    """
    # Convert degrees and minutes to radians
    def to_radians(degrees):
        PI = 3.141592
        deg = int(degrees)
        min = degrees - deg
        return PI * (deg + 5.0 * min / 3.0) / 180.0

    lat1_rad = to_radians(deg_lat1)
    lon1_rad = to_radians(deg_lon1)
    lat2_rad = to_radians(deg_lat2)
    lon2_rad = to_radians(deg_lon2)

    RRR = 6378.388
    q1 = math.cos(lon1_rad - lon2_rad)
    q2 = math.cos(lat1_rad - lat2_rad)
    q3 = math.cos(lat1_rad + lat2_rad)
    distance = int(RRR * math.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0)
    
    return distance

def att_distance(x1, y1, x2, y2) -> int:
    """
    Calculates the pseudo-Euclidean distance between two points, rounded to the nearest integer, for TSP instances of type ATT.

    Parameters:
    - x1, y1: Coordinates of the first point.
    - x2, y2: Coordinates of the second point.

    Returns:
    - The rounded pseudo-Euclidean distance.
    """
    rij = math.sqrt((math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2)) / 10.0)
    tij = round(rij + 0.5)
    return tij

def parse_explicit_distances(explicit_distances, edge_weight_format, dimension) -> list:
    """
    Parses explicit distances based on the format and dimension specified, organizing them into a list of tuples.
    
    Parameters:
    - explicit_distances: A list of explicit distances.
    - edge_weight_format: The format of the explicit distances.
    - dimension: The dimension of the TSP instance.
    
    Returns:
    - A list of tuples containing the distances between nodes.
    """
    distances = []
    if edge_weight_format == "FULL_MATRIX":
        for i in range(dimension):
            for j in range(i + 1, dimension):
                distances.append((i+1, j+1, explicit_distances[i * dimension + j]))
    elif edge_weight_format == "LOWER_DIAG_ROW":
        index = 0
        for i in range(dimension):
            for j in range(i + 1):
                if i != j:
                    distances.append((j+1, i+1, explicit_distances[index]))
                index += 1
    return distances

def calculate_distances(node_coords, edge_weight_type) -> list:
    """
    Calculates the distances between nodes based on the specified edge weight type.
    
    Parameters:
    - node_coords: A dictionary containing node IDs and their coordinates.
    - edge_weight_type: The type of edge weight to be used.
    
    Returns:
    - A list of tuples containing the distances between nodes.
    """
    distances = []
    for i, (x1, y1) in node_coords.items():
        for j, (x2, y2) in node_coords.items():
            if i < j:
                if edge_weight_type == "EUC_2D":
                    dist = euclidean_distance(x1, y1, x2, y2)
                elif edge_weight_type == "GEO":
                    dist = geo_distance(x1, y1, x2, y2)
                elif edge_weight_type == "ATT":
                    dist = att_distance(x1, y1, x2, y2)
                distances.append((i, j, dist))
    return distances

def save_edge_file(distances, output_filename) -> None:
    """
    Saves a list of distances to a file.
    
    Parameters:
    - distances: A list of tuples containing the distances between nodes.
    - output_filename: The name of the file to be saved.
    """
    with open(output_filename, 'w') as f:
        for i, j, dist in distances:
            f.write(f"{i}\t{j}\t{dist}\n")

def main():
    input_folder = "../tsp_files/"
    output_folder = "../networkx_tsp_files/"
    os.makedirs(output_folder, exist_ok=True)
    
    for tsp_file in os.listdir(input_folder):
        if tsp_file.endswith(".tsp"):
            filepath = os.path.join(input_folder, tsp_file)
            node_coords, edge_weight_type, edge_weight_format, explicit_distances, dimension = parse_tsp_file(filepath)
            if edge_weight_type == "EXPLICIT":
                distances = parse_explicit_distances(explicit_distances, edge_weight_format, dimension)
            else:
                distances = calculate_distances(node_coords, edge_weight_type)
            output_filename = os.path.join(output_folder, tsp_file.replace(".tsp", ".edges"))
            save_edge_file(distances, output_filename)

if __name__ == "__main__":
    main()