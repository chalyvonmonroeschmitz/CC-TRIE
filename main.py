import math
import numpy
from CC_Trie import Trie


class EnhancedTrieWithGraph(Trie):
    def get_matrice_graph_with_results(self):
        """
        Create a matrix graph of all TrieNodes and compute the equation for connected nodes.
        Returns the graph and outputs of all calculations.
        """
        matrix_graph = {}  # To store connections and outputs

        def traverse_and_build(node, parent_word, parent_params):
            # Initialize a new entry for the current node
            current_node_key = parent_word  # The word represented by this node
            matrix_graph[current_node_key] = {"connections": [], "results": []}

            # Traverse children (connected nodes)
            for char, child_node in node.children.items():
                # Build the word as we traverse
                child_word = parent_word + char
                child_params = child_node.data[0] if child_node.data else {"d": [0, 0, 0], "i": [0, 0, 0],
                                                                           "h": [0, 0, 0]}

                # Connect parent to child
                matrix_graph[current_node_key]["connections"].append(child_word)

                # If there's a parent, child, and current node, calculate the equation
                if parent_params and child_params and node.data:
                    # Extract weights for the nodes involved in the equation
                    d = parent_params.get("d", [0, 0, 0])
                    i = node.data[0].get("i", [0, 0, 0])
                    h = child_params.get("h", [0, 0, 0])

                    # Calculate the formula
                    formula_result = (
                                             3 * (
                                             sum(d) + sum(i) + sum(h)
                                     ) + 50
                                     ) * (1 / math.pi) / 1000

                    # Add the result to the matrix graph
                    matrix_graph[current_node_key]["results"].append({
                        "child": child_word,
                        "formula_result": formula_result
                    })

                # Recursively process the child's children
                traverse_and_build(child_node, child_word, child_params)

        # Start traversal from the root and build the graph and equation outputs
        traverse_and_build(self.root, "", None)
        return matrix_graph



def main():
    # Initialize the Trie
    trie = Trie()

    # 6. Test `read_in_dictionary` Method (Optional depending on input file)
    print("\nTesting `read_in_dictionary` method...")
    file_name = "Data/elements_table_v20.txt"  # Update to the path of the dictionary file, if available
    try:
        trie = trie.read_in_dictionary(file_name)
        print(f"Dictionary loaded successfully from {file_name}!")
        print(f"{trie.get_words()}")
    except FileNotFoundError:
        print(f"File {file_name} not found. Skipping this test.")

# Create Trie and populate it
    trie = EnhancedTrieWithGraph()
    trie.insert("abc", {"d": [1, 1, 1], "i": [2, 2, 2], "h": [3, 3, 3]})
    trie.insert("abd", {"d": [4, 4, 4], "i": [0, 0, 0], "h": [1, 1, 1]})
    trie.insert("abe", {"d": [2, 2, 2], "i": [1, 1, 1], "h": [1, 1, 1]})
    trie.insert("xyz", {"d": [0, 0, 0], "i": [0, 0, 0], "h": [0, 0, 0]})  # Non-matching

# Generate and print the matrix graph
    matrix_graph = trie.get_matrice_graph_with_results()

    for node, details in matrix_graph.items():
        print(f"Node: {node}")
        print(f"  Connections: {details['connections']}")
        print(f"  Results:")
        for result in details["results"]:
            print(f"    -> Child: {result['child']}, Formula Result: {result['formula_result']:.6f}")


# Call the main function to run the tests
if __name__ == "__main__":
    main()