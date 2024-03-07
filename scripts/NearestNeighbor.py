import networkx as nx
import TsplibNwxUtils as util

def nearest_neighbor_fixed(G, start_node):
    path = [start_node]
    total_weight = 0
    visited = set([start_node])

    while len(visited) < len(G.nodes):
        current_node = path[-1]
        possible_edges = [(n, G[current_node][n]['weight']) for n in G.neighbors(current_node) if n not in visited]
        if not possible_edges:
            break  # No unvisited neighbors, exit loop
        next_node, weight = min(possible_edges, key=lambda x: x[1])
        path.append(next_node)
        total_weight += weight
        visited.add(next_node)

    return path, total_weight
  
def all_nearest_neighbor(G):
  best_path = []
  best_weight = float('inf')
  best_starting_node = None

  for node in G.nodes():
      path, weight = nearest_neighbor_fixed(G, node)
      if weight < best_weight:
          best_path = path
          best_weight = weight
          best_starting_node = node

  return best_starting_node, best_path, best_weight

if __name__ == "__main__":
   
    filename = "../networkx_tsp_files/ulysses16.edges"
    edges = util.parse_edges_file(filename)
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    
    opt_tour_filename = "../tour_files/ulysses16.opt.tour"
    optimal_path = util.parse_opt_tour_file(opt_tour_filename)
    closed_optimal_path = util.close_path(G, optimal_path)
    closed_optimal_path_length = util.calculate_path_length(G, closed_optimal_path)
    
    start_node, nnh_path, weight = all_nearest_neighbor(G)
    closed_nnh_path = util.close_path(G, nnh_path)
    closed_nnh_path_length = util.calculate_path_length(G, closed_nnh_path)
    pos = nx.spring_layout(G)  # Calculate layout for visual representation
    print(f"Nearest neighbor path: {closed_nnh_path}")
    print(f"Nearest neighbor path length: {closed_nnh_path_length}")
    print(f"Optimal path: {closed_optimal_path}")
    print(f"Optimal path length: {closed_optimal_path_length}")
    util.draw_graph(G, pos, title=f"Graph with nearest neighbor path and length {closed_nnh_path_length}", path=closed_nnh_path, edge_labels=False)
    util.draw_graph(G, pos, title=f"Graph with optimal path and length {closed_optimal_path_length}", path=closed_optimal_path, edge_labels=False, onlyShowPath=True)
  