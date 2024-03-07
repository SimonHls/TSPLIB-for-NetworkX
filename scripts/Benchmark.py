import os
import csv
import TsplibNwxUtils as util
import networkx as nx
import datetime
import time
from NearestNeighbor import all_nearest_neighbor  # Import the heuristic function
from BruteForce import brute_force  # Import the brute-force function
from BranchAndBound import branch_and_bound_tsp_optimized  # Import the branch-and-bound function

def export_results(results, base_folder="./benchmark_results", base_name="benchmark_results"):
    """
    Exports the benchmark results to a new CSV file with a unique timestamp on every execution.

    Args:
        results (list): The benchmark results to be exported.
        base_folder (str): The folder to save the CSV file.
        base_name (str): The base name for the CSV file.

    Returns:
        None
    """
    timestamp = datetime.datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
    # Ensure the directory exists
    os.makedirs(base_folder, exist_ok=True)
    csv_filename = os.path.join(base_folder, f"{base_name}{timestamp}.csv")
    
    fieldnames = ["tsp_name", "optimal_tour", "optimal_length", "heuristic_tour", "heuristic_length", "deviation", "execution_time", "error"]
    with open(csv_filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"Benchmark results exported to {csv_filename}")

def benchmark_heuristic(heuristic):
    """
    Benchmarks a heuristic for solving TSPs by comparing the generated path to the optimal solution.

    Args:
        heuristic (function): The heuristic function to benchmark.

    Returns:
        None
    """
    results = []
    tsp_files_folder = "./benchmark_tsp_files"
    tour_files_folder = "../tour_files"

    for filename in os.listdir(tsp_files_folder):
        if filename.endswith(".edges"):
            current_tsp_filename = os.path.join(tsp_files_folder, filename)
            opt_tour_filename = os.path.join(tour_files_folder, filename.replace(".edges", ".opt.tour"))
            print(f"Benchmarking {filename}...")

            try:
                edges = util.parse_edges_file(current_tsp_filename)
                G = nx.Graph()
                G.add_weighted_edges_from(edges)

                start_time = time.time()
                heuristic_path = heuristic(G)  # Perform the heuristic
                end_time = time.time()
                execution_time = end_time - start_time

                if os.path.exists(opt_tour_filename):
                    optimal_path = util.parse_opt_tour_file(opt_tour_filename)

                    try:
                        closed_optimal_path = list(util.close_path(G, optimal_path))
                        closed_optimal_path_length = util.calculate_path_length(G, closed_optimal_path)

                        closed_heuristic_path = list(util.close_path(G, heuristic_path[1]))
                        closed_heuristic_path_length = util.calculate_path_length(G, closed_heuristic_path)

                        deviation = (closed_heuristic_path_length - closed_optimal_path_length) / closed_optimal_path_length

                        result = {
                            "tsp_name": filename,
                            "optimal_tour": closed_optimal_path,
                            "optimal_length": closed_optimal_path_length,
                            "heuristic_tour": closed_heuristic_path,
                            "heuristic_length": closed_heuristic_path_length,
                            "deviation": deviation,
                            "execution_time": execution_time,
                            "error": ""
                        }
                    except Exception as e:
                        result = {
                            "tsp_name": filename,
                            "optimal_tour": optimal_path,
                            "optimal_length": "",
                            "heuristic_tour": heuristic_path[1],
                            "heuristic_length": "",
                            "deviation": "",
                            "execution_time": execution_time,
                            "error": str(e)
                        }
                else:
                    result = {
                        "tsp_name": filename,
                        "optimal_tour": "",
                        "optimal_length": "",
                        "heuristic_tour": heuristic_path[1],
                        "heuristic_length": heuristic_path[2],
                        "deviation": "",
                        "execution_time": execution_time,
                        "error": f"Optimal tour file not found: {opt_tour_filename}"
                    }

                results.append(result)

            except Exception as e:
                result = {
                    "tsp_name": filename,
                    "optimal_tour": "",
                    "optimal_length": "",
                    "heuristic_tour": "",
                    "heuristic_length": "",
                    "deviation": "",
                    "execution_time": "",
                    "error": str(e)
                }
                results.append(result)
                
    return results

# Example usage
results = benchmark_heuristic(branch_and_bound_tsp_optimized)
export_results(results)