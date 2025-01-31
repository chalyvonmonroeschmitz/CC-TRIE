# periodictable version 2.0 - https://periodictable.readthedocs.io/
import periodictable

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
    def __init__(self, mass, number=0, symbol="TBA", name="TBA", formula="TBA"):
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

def main():
    # Initialize the Trie
    trie = Trie()

    # 6. Test `read_in_dictionary` Method (Optional depending on input file)
    print("\nTesting `read_in_dictionary` method...")
    file_name = "Data/elements_table_v20.txt"  # Update to the path of the dictionary file, if available
    try:
        trie = trie.read_in_dictionary(file_name)
        print(f"Dictionary loaded successfully from {file_name}!")
    except FileNotFoundError:
        print(f"File {file_name} not found. Skipping this test.")

    print(f"\nAll Formulas in Trie: {trie.get_words()}")
    formua = "Na"
    print(f"\nCompound Data in Trie {formua}: {trie.get_node(formua).data[0].symbol}, mass: {trie.get_node(formua).data[0].mass}")
    print("\nAll tests completed!")


# Call the main function to run the tests
if __name__ == "__main__":
    main()
