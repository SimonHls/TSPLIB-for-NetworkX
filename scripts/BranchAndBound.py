import networkx as nx
import heapq
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def calculate_lower_bound(G, path, unvisited):
    if not unvisited:
        return 0  # Return 0 if there are no unvisited nodes to avoid min() error
   
    # Original lower bound calculation code remains unchanged
    H = G.subgraph(unvisited)
    mst_weight = sum(edge[2]['weight'] for edge in nx.minimum_spanning_edges(H, data=True))
    last_in_path = path[-1]
    min_edge_to_unvisited = min(G.edges[last_in_path, v]['weight'] for v in unvisited)
    min_edge_from_start = min(G.edges[path[0], v]['weight'] for v in unvisited)
    return mst_weight + min_edge_to_unvisited + min_edge_from_start

def branch_and_bound_worker(G, queue_item):
    cost, path, unvisited = queue_item
    if not unvisited:
        total_cost = cost + G[path[-1]][path[0]]['weight']
        return total_cost, path
    else:
        best_cost = float('inf')
        best_path = None
        for v in unvisited:
            next_path = path + [v]
            next_unvisited = unvisited - {v}
            next_cost = cost + G[path[-1]][v]['weight']
            lower_bound = next_cost + calculate_lower_bound(G, next_path, next_unvisited)
            if lower_bound < best_cost:
                best_cost, best_path = branch_and_bound_worker(G, (lower_bound, next_path, next_unvisited))
        return best_cost, best_path

def branch_and_bound_tsp_optimized(G, max_workers=4):
    nodes = list(G.nodes())
    Q = [(0, [nodes[0]], set(nodes[1:]))]
    best_cost = float('inf')
    best_path = None
    total_queue_items = len(Q)
    processed_items = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        with tqdm(total=total_queue_items, desc="Processing queue", unit="item", dynamic_ncols=True) as progress_bar:
            while Q:
                queue_item = heapq.heappop(Q)
                futures.append(executor.submit(branch_and_bound_worker, G, queue_item))
                processed_items += 1
                progress_bar.set_postfix(best_cost=best_cost, processed=processed_items, total=total_queue_items)
                progress_bar.update(1)

                if len(futures) >= max_workers:
                    for future in as_completed(futures):
                        cost, path = future.result()
                        if cost < best_cost:
                            best_cost = cost
                            best_path = path
                            progress_bar.set_postfix(best_cost=best_cost, processed=processed_items, total=total_queue_items)
                    futures = []

                # Add new queue items to the total count
                total_queue_items += len(futures)
                progress_bar.total = total_queue_items

            for future in as_completed(futures):
                cost, path = future.result()
                if cost < best_cost:
                    best_cost = cost
                    best_path = path
                    progress_bar.set_postfix(best_cost=best_cost, processed=processed_items, total=total_queue_items)

    # also available: return best_path, best_cost
    return best_path