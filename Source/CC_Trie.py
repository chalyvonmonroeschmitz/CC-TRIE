# periodictable version 2.0 - https://periodictable.readthedocs.io/
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class ElementNode:

    def __init__(self):
        self.children = {}
        self.is_end = False
        self.data = []

    def contains_key(self, char):
        return char in self.children

    def add_child(self, char, node):
        self.children[char] = node

    def get_child(self, char):
        return self.children.get(char)

    def add_data(self, data):
        self.data.append(data)


class Compound:
    def __init__(self, number=0, symbol="TBA", name="TBA", mass=float(0.00), formula="TBA"):
        self.number = number
        self.symbol = symbol
        self.name = name
        self.mass = mass
        self.formula = formula

    def set_number(self, number):
        self.number = number

    def set_mass(self, mass):
        self.mass = mass

    def get_mass(self):
        return self.mass

    def get_symbol(self):
        return self.symbol

    def set_symbol(self, symbol):
        self.symbol = symbol

    def set_formula(self, formula):
        self.formula = formula

    def get_formula(self):
        return self.formula

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

class Trie:
    def __init__(self):
        self.root = ElementNode()

    def insert(self, string, data):
        """
        Inserts a string and returns the last node where the string ends.
        """
        node = self.root
        for char in string:
            if not node.contains_key(char):
                node.add_child(char, ElementNode())
            node = node.get_child(char)
        node.add_data(data)
        node.is_end = True
        return node

    def get_node(self, string):
        """
        Search for a prefix in the trie and return the final node it represents.
        """
        node = self.root
        for char in string:
            if node.contains_key(char):
                node = node.get_child(char)
            else:
                return None
        return node

    def get(self, string):
        """
        Search for a complete word in the trie and return the final node,
        if and only if it is marked as an end-of-word node.
        """
        node = self.get_node(string)
        if node and node.is_end:
            return node
        return None

    def starts_with(self, prefix):
        """
        Check if any words in the trie start with the given prefix.
        """
        return self.get_node(prefix) is not None

    def get_words(self, prefix=""):
        """
        Retrieve a list of all words in the trie starting with a given prefix.
        """
        result = []
        start_node = self.get_node(prefix)
        if start_node:
            self._add_all_words(start_node, prefix, result)
        return result

    def get_alphabetical_list_with_prefix(self, prefix):
        """
        Return an alphabetically sorted list of all words that begin with the given prefix.
        """
        return sorted(self.get_words(prefix))  # Sorting the words alphabetically

    def _add_all_words(self, node, word, result):
        """
        Helper method to recursively add all words starting from a given node.
        """
        if node.is_end:
            result.append(word)

        for char, next_node in node.children.items():
            self._add_all_words(next_node, word + char, result)

    def get_most_frequent_word_with_prefix(self, prefix):
        """
        Finds the most frequently occurring word that starts with the given prefix.
        """
        words = self.get_words(prefix)
        max_freq = -1
        top_word = None

        for word in words:
            mass = self.get(word).data[0].get_mass()  # Assuming data[0] has mass
            if mass > max_freq:
                max_freq = mass
                top_word = word

        return top_word

    def read_in_dictionary(self, file_name):
        """
        Reads a dictionary from a file and inserts all words into the trie.
        """
        trie = Trie()
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    try:
                        number, symbol, name, mass, formula = line.split()
                        number = int(number)
                        symbol = symbol
                        name = name
                        mass = float(mass)
                        formula = formula
                        data = Compound(number, symbol, name, mass, formula)
                        trie.insert(formula, data)
                    except ValueError:
                        continue  # Skip malformed lines
        except FileNotFoundError as e:
            print(f"Error: {e}")
        return trie

def plot_element_masses(trie):
    """
    Plots a Cartesian graph of chemical elements and their corresponding masses.
    """
    elements = trie.get_words()  # Get all element formulas from the trie
    element_masses = {}

    # Sum up masses for each element
    for e in elements:
        node = trie.get(e)
        if node and node.data:  # Ensure the node has data
            total_mass = sum(compound.get_mass() for compound in node.data)
            element_masses[e] = total_mass

    # Sort elements alphabetically for better visualization
    sorted_elements = sorted(element_masses.keys())
    sorted_masses = [element_masses[element] for element in sorted_elements]

    # Plot the Cartesian graph
    plt.figure(figsize=(12, 6))
    plt.bar(sorted_elements, sorted_masses, color='skyblue')
    plt.xlabel('Element Formula', fontsize=12)
    plt.ylabel('Total Mass', fontsize=12)
    plt.title('Element Mass Distribution', fontsize=14)
    plt.xticks(rotation=90, fontsize=10)
    plt.tight_layout()
    plt.show()
    plt.close()


def create_summation_matrix(trie, elements, x, y, z):
    """
    Creates a matrix where each cell contains the recursive summation of the starting element `x`
    and adds up all instances of elements `y` and `z` recursively.

    Args:
        trie: The Trie instance containing element data.
        elements: A list of all element formulae in the trie.
        x: Starting element.
        y: First element to add recursively.
        z: Second element to add recursively.

    Returns:
        A numpy 2D array (matrix) with the calculated sums.
    """
    size = len(elements)
    matrix = np.zeros((size, size))  # Create an empty square matrix

    for i, xi in enumerate(elements):  # Iterate over rows (elements as starting points)
        for j, xj in enumerate(elements):  # Iterate over columns (elements to sum)
            # Perform recursive summation
            matrix[i, j] = recursive_sum(trie, xi, xj, y, z)

    return matrix


def recursive_sum(trie, start, current, y, z, depth=0):
    """
    Recursively sums up the specified elements `y` and `z` starting from `start` and `current`.
    Limits recursion depth to avoid infinite loops.

    Args:
        trie: The Trie instance containing element data.
        start: The starting element.
        current: The current element being processed.
        y: First element to add.
        z: Second element to add.
        depth: Current recursion depth.

    Returns:
        The recursive summation value.
    """
    # Limit recursion depth
    if depth > 10:  # Prevent infinite recursion
        return 0

    node_start = trie.get(start)
    node_current = trie.get(current)

    if not node_start or not node_current:
        return 0  # Element not found in Trie

    # Calculate mass of current node's data
    total_mass = 0
    for compound in node_current.data:
        total_mass += compound.get_mass()

    # Recursive call for children `y` and `z`
    sum_y = recursive_sum(trie, start, y, y, z, depth + 1)
    sum_z = recursive_sum(trie, start, z, y, z, depth + 1)

    return total_mass + sum_y + sum_z


def plot_matrix(matrix, elements):
    """
    Plots the summation matrix as a heatmap using a ROYGBIV-like color spectrum, optimized for full-screen 1080p viewing,
    with increased padding to ensure labels are spaced and clearly visible.

    Args:
        matrix: A 2D numpy array (matrix) containing the summation values.
        elements: A list of element names corresponding to the matrix rows and columns.
    """
    plt.figure(figsize=(64, 64))  # Larger figure size for extra spacing (16:9 ratio)

    # Heatmap visualization with updated ROYGBIV colormap ('rainbow')
    plt.imshow(matrix, cmap='rainbow', interpolation='nearest')
    cbar = plt.colorbar(label='Summation Value')  # Add the color bar

    # Adjust tick labels for x and y axes with clearer spacing
    plt.xticks(ticks=np.arange(len(elements)), labels=elements, rotation=75, ha='right', fontsize=12)
    plt.yticks(ticks=np.arange(len(elements)), labels=elements, fontsize=12)

    # Add axis labels and title with extra spacing
    plt.xlabel('Element (Columns)', fontsize=16, labelpad=40)  # Increase label padding
    plt.ylabel('Element (Rows)', fontsize=16, labelpad=40)
    plt.title('Recursive Summation Matrix', fontsize=22, pad=50)  # Add extra padding to title

    # Adjust layout to minimize overlap
    plt.tight_layout(pad=8.0)  # Higher padding for tight layout
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)  # Adjust figure margins

    # Display the matrix plot
    plt.show()
    plt.close()


"""
This function will run for a prolonged period of time to display every element and it's corresponding 3 dimensional mass
Advisable to use the find the sum of a specific element
"""
def compute_and_plot_sum_tables(elements):
    """
    Computes the sum of element x, y, and z and displays the sum values
    in a table-like matrix for each combination of x, y, and z elements.

    Args:
        elements: A list of element names. The corresponding numeric values
                  are assigned as sequential integers (e.g., 1, 2, 3, ...).
    """
    # Assign numeric values to each element
    element_values = np.arange(1, len(elements) + 1)

    # Create an empty 3D matrix to store sums for each combination of x, y, z
    n = len(elements)
    sum_matrix = np.zeros((n, n, n))

    # Compute the summation table for all x, y, z combinations
    for x in range(n):
        for y in range(n):
            for z in range(n):
                sum_matrix[x, y, z] = element_values[x] + element_values[y] + element_values[z]

    # Now plot the 2D sum table for each fixed z value
    for z in range(n):
        plt.figure(figsize=(64, 64))
        plt.title(f"Sum Matrix for z={elements[z]} (Value={element_values[z]})", fontsize=16, pad=20)
        sns.heatmap(sum_matrix[:, :, z], cmap='rainbow', annot=True, fmt='.0f', cbar_kws={'label': 'Summation Value'},
                    square=True, linewidths=0.5, linecolor='white')

        # Set up axis labels
        plt.xticks(ticks=np.arange(n) + 0.5, labels=elements, fontsize=10, rotation=45, ha='right')
        plt.yticks(ticks=np.arange(n) + 0.5, labels=elements, fontsize=10)
        plt.xlabel("y Element (Columns)", fontsize=12, labelpad=10)
        plt.ylabel("x Element (Rows)", fontsize=12, labelpad=10)

        # Add spacing and show the plot
        plt.tight_layout(pad=4)
        plt.show()
        plt.close()


def plot_sum_for_single_element_x(elements, x_element):
    """
    Plots the summation values for a single element x in the 3D table x, y, z.

    Args:
        elements: A list of element names.
        x_element: The specific element name to be plotted.
    """
    # Assign numeric values to each element
    element_values = np.arange(1, len(elements) + 1)
    x_index = elements.index(x_element)

    # Create an empty 2D matrix to store sums for each combination of y, z with fixed x
    n = len(elements)
    sum_matrix = np.zeros((n, n))

    # Compute the summation table for the fixed x combination with y, z
    for y in range(n):
        for z in range(n):
            sum_matrix[y, z] = element_values[x_index] + element_values[y] + element_values[z]

    # Plot the 2D sum table for the fixed x value
    plt.figure(figsize=(64, 64))
    plt.title(f"Sum Matrix for x={x_element} (Value={element_values[x_index]})", fontsize=16, pad=20)
    sns.heatmap(sum_matrix, cmap='rainbow', annot=True, fmt='.0f', cbar_kws={'label': 'Summation Value'},
                square=True, linewidths=0.5, linecolor='white')

    # Set up axis labels
    plt.xticks(ticks=np.arange(n) + 0.5, labels=elements, fontsize=10, rotation=45, ha='right')
    plt.yticks(ticks=np.arange(n) + 0.5, labels=elements, fontsize=10)
    plt.xlabel("z Element (Columns)", fontsize=12, labelpad=10)
    plt.ylabel("y Element (Rows)", fontsize=12, labelpad=10)

    # Add spacing and show the plot
    plt.tight_layout(pad=4)
    plt.show()
    plt.close()

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
        x = trie.get_node("He").data[0].symbol if elements else None  # Starting element (e.g., first from the list)
        y = "H"  # Example element to sum recursively
        z = "U"  # Another example element to sum recursively

        if x is None:
            print("No valid elements found in the Trie.")
            return

        # Create summation matrix
        matrix = create_summation_matrix(trie, elements, x, y, z)
        # Plot the resulting matrix
        plot_matrix(matrix, elements)
        # compute sum tables x y z for element x
        plot_sum_for_single_element_x(elements, x)

    except FileNotFoundError:
        print(f"File {file_name} not found. Please provide a valid file path.")

# Call the main function to run the tests
if __name__ == "__main__":

    main()
