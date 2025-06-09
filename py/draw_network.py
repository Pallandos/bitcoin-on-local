from network_info import visualize_network
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path_argument = sys.argv[1]
        visualize_network(path_argument)
    else:
        print("[INFO ] No path argument provided, using default path.")
        visualize_network()