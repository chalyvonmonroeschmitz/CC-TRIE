import math
import CC_Trie
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

    # Load element data from file (Update file path accordingly)
    file_name = "Data/elements_table_v20.txt"
    try:
        trie = trie.read_in_dictionary(file_name)

        # Get all elements from the trie
        elements = trie.get_words()

        # Define x, y, z
        x = elements[0] if elements else None  # Starting element (e.g., first from the list)
        y = "H"  # Example element to sum recursively
        z = "O"  # Another example element to sum recursively

        if x is None:
            print("No valid elements found in the Trie.")
            return

        # Create summation matrix
        matrix = CC_Trie.create_summation_matrix(trie, elements, x, y, z)

        # Plot the resulting matrix
        CC_Trie.plot_matrix(matrix, elements)
        # compute sum tables x y z elements
        CC_Trie.compute_and_plot_sum_tables(elements)

    except FileNotFoundError:
        print(f"File {file_name} not found. Please provide a valid file path.")

# Call the main function to run the tests
if __name__ == "__main__":
    main()