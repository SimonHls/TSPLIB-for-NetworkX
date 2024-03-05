import networkx as nx
import matplotlib.pyplot as plt

def parse_edges_file(filename) -> list:
    """Parse an .edges file and return a list of edges with weights.
    Parameters:
    - filename: The name of the .edges file to parse.
    
    Returns:
    - A list of edges, where each edge is a tuple (node1, node2, weight).
    """
    edges = []
    with open(filename, 'r') as file:
        for line in file:
            node1, node2, weight = line.strip().split()
            edges.append((int(node1), int(node2), float(weight)))
    return edges
  
def parse_opt_tour_file(filename) -> list:
    """
    Parse an optimal tour file (.opt.tour) and return the sequence of nodes in the tour.

    Parameters:
    - filename: The name of the .opt.tour file.

    Returns:
    - A list of nodes representing the optimal tour.
    """
    tour = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        
        # Find the start of the TOUR_SECTION
        start_index = lines.index("TOUR_SECTION\n") + 1
        # Process each line until '-1' or 'EOF' is encountered
        for line in lines[start_index:]:
            if line.strip() in ('-1', 'EOF'):
                break  # Stop parsing if '-1' or 'EOF' is encountered
            tour.extend(map(int, line.strip().split()))
            
    return tour

def draw_graph(G, pos, title='Graph Visualization', path=None, edge_labels=False, onlyShowPath=False) -> None:
    """
    Draw the graph with optional title and path. Can optionally show only the path.

    Parameters:
    - G: The graph to be drawn.
    - pos: The position layout for nodes in the graph.
    - title (optional): Title of the graph.
    - path (optional): A list of nodes representing the path to highlight. e.g. [1, 2, 3, 4, 5]
    - edge_labels (optional): If True, display edge weights.
    - onlyShowPath (optional): If True, only the path is rendered.
    """
    plt.figure(figsize=(10, 8))
    plt.tight_layout()
    plt.title(title)
    
    if onlyShowPath and path:
        # Draw only the path if onlyShowPath is True
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=3)
    else:
        # Draw the graph
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', edge_color='k', linewidths=1, width=2)
        
        # Optionally draw edge labels
        if edge_labels:
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        
        # Highlight the path if provided
        if path:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=3)
    
    plt.show()

def calculate_path_length(G, path):
    """
    Calculate the total length of a path in a weighted graph.

    Parameters:
    - G: A NetworkX graph with weighted edges.
    - path: A list of node IDs representing the path.

    Returns:
    - The total length of the path.
    """
    path_length = 0
    # Iterate through pairs of consecutive nodes in the path
    for i in range(len(path) - 1):
        node1, node2 = path[i], path[i + 1]
        # Sum up the edge weights between consecutive nodes
        edge_weight = G[node1][node2]['weight']
        path_length += edge_weight
    
    return path_length

def close_path(G, path):
    """
    Connects the last node in the path back to the first node, if not already connected,
    to form a closed loop representing a round trip.

    Parameters:
    - G: The NetworkX graph.
    - path: A list of nodes representing the path.
    
    Returns:
    - A list of nodes representing the closed path.
    """
    if path[0] != path[-1]:  # Check if path is not already closed
        # Calculate the weight of the edge from the last node back to the first
        weight = G[path[-1]][path[0]]['weight'] if G.has_edge(path[-1], path[0]) else 0
        # Add the first node at the end of the path to close the loop
        closed_path = path + [path[0]]
    else:
        closed_path = path  # Path is already closed
        weight = 0  # No additional weight required to close the path

    return closed_path, weight


if __name__ == "__main__":
    opt_tour_filename = "../tour_files/ulysses16.opt.tour"
    optimal_path = parse_opt_tour_file(opt_tour_filename)
    filename = "../networkx_tsp_files/ulysses16.edges"
    edges = parse_edges_file(filename)
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    pos = nx.spring_layout(G)  # Calculate layout for visual representation
    # draw_graph(G, pos)
    # example_path = [1, 2, 3, 4, 5]
    optimal_path_length = calculate_path_length(G, optimal_path)
    draw_graph(G, pos, title=f"Graph with optimal path and length {optimal_path_length}", path=optimal_path, edge_labels=False)
