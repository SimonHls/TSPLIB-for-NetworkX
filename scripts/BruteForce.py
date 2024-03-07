import itertools
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Authors note: This is a brute-force solution to the TSP problem. It is not efficient and should not be used for large instances.
# A large instance is already around 10 nodes...
# It is included here for educational purposes only.


def calculate_path_weight(G, path):
    weight = 0
    for i in range(len(path) - 1):
        weight += G[path[i]][path[i + 1]]['weight']
    weight += G[path[-1]][path[0]]['weight']  # Complete the tour
    return weight

def brute_force_path_worker(G, path):
    return path, calculate_path_weight(G, path)

def brute_force(G, max_workers=12, batch_size=1000000):
    nodes = list(G.nodes)
    # Fix the first node and generate permutations of the rest
    permutations = itertools.permutations(nodes[1:])
   
    optimal_path = None
    optimal_weight = float('inf')
   
    try:
        total_permutations = math.factorial(len(nodes) - 1)
        with tqdm(total=total_permutations, desc="Calculating paths", unit="path") as progress_bar:
            while True:
                batch = list(itertools.islice(permutations, batch_size))
                if not batch:
                    break
               
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = [executor.submit(brute_force_path_worker, G, (nodes[0],) + path) for path in batch]
                   
                    for future in as_completed(futures):
                        path, weight = future.result()
                        if weight < optimal_weight:
                            optimal_path = path
                            optimal_weight = weight
                            print(f"\rCurrent shortest path: {optimal_path}, Weight: {optimal_weight}", end="", flush=True)
               
                progress_bar.update(len(batch))
    except KeyboardInterrupt:
        print("\nInterrupted by user. Stopping the brute-force search.")
   
    print(f"\nFinal shortest path: {optimal_path}, Weight: {optimal_weight}")
    return list(optimal_path) if optimal_path else None