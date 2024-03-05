import math

def parse_tsp_file(filename):
    """Parse a TSP file and return node coordinates.
    
    Parameters:
    - filename: The name of the TSP file.
    
    Returns:
    - A dictionary where the keys are node IDs and the values are (x, y) coordinates.
    """
    node_coordinates = {}
    edge_weight_type = ''
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
        # Find and process the EDGE_WEIGHT_TYPE
        for line in lines:
            if line.startswith("EDGE_WEIGHT_TYPE"):
                edge_weight_type = line.split(":")[1].strip()
                
        # Find the start of the NODE_COORD_SECTION
        try:
            start_index = lines.index("NODE_COORD_SECTION\n") + 1
        except ValueError:
            start_index = lines.index("NODE_COORD_SECTION\r\n") + 1  # For Windows-style line endings
            
        # Process each line until 'EOF' or another non-numeric line is encountered
        for line in lines[start_index:]:
            if "EOF" in line or line.strip() == '':
                break  # Stop parsing if 'EOF' or an empty line is encountered
            parts = line.strip().split()
            try:
                node_id = int(parts[0])
                x, y = float(parts[1]), float(parts[2])
                node_coordinates[node_id] = (x, y)
            except ValueError:
                # This handles any lines that don't match the expected format
                print(f"Skipping line: {line.strip()}")
                continue
                
    return node_coordinates, edge_weight_type
  
  
def choose_distance_calculator(edge_weight_type):
    if edge_weight_type == "ATT":
        return att_distance
    elif edge_weight_type == "GEO":
        return geo_distance
    else:
        raise ValueError("Unsupported EDGE_WEIGHT_TYPE")

from math import cos, acos, radians

import math

def geo_distance(deg_lat1, deg_lon1, deg_lat2, deg_lon2):
    """Calculate geographical distance using corrected interpretation for degrees and minutes.
    
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


def att_distance(x1, y1, x2, y2):
    """
    Calculate the pseudo-Euclidean distance between two nodes for the ATT format.
    
    Parameters:
    - x1, y1: Coordinates of the first node.
    - x2, y2: Coordinates of the second node.
    
    Returns:
    - The pseudo-Euclidean distance rounded to the nearest whole number.
    """
    dx, dy = x1 - x2, y1 - y2
    rij = math.sqrt((dx**2 + dy**2) / 10.0)
    tij = round(rij + 0.5)
    return tij


def save_edges_file(edges, output_filename):
    """Save pre-calculated edges to a file."""
    with open(output_filename, 'w') as f:
        for edge in edges:
            f.write(f"{edge[0]} {edge[1]} {edge[2]}\n")


def main():
    filename = "ulysses16"
    input_filename = "../tsp_files/" + filename + ".tsp"
    output_filename = "../networkx_tsp_files/" + filename + ".edges"

    # Parse the TSP file to get node coordinates and edge weight type
    node_coordinates, edge_weight_type = parse_tsp_file(input_filename)
    
    # Choose the appropriate distance calculator
    distance_calculator = choose_distance_calculator(edge_weight_type)
    
    print(f"Using {edge_weight_type} distance calculator")
    
    # Pre-calculate the edges with distances
    edges = []
    for i, coord1 in node_coordinates.items():
        for j, coord2 in node_coordinates.items():
            if i < j:
                distance = distance_calculator(coord1[0], coord1[1], coord2[0], coord2[1])
                edges.append((i, j, distance))
    
    # Save the edges to a file
    save_edges_file(edges, output_filename)


if __name__ == "__main__":
    main()
