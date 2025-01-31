class TrieNode:
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


class TrieData:
    def __init__(self, frequency):
        self.frequency = frequency
        self.rank = None

    def set_rank(self, rank):
        self.rank = rank

    def get_frequency(self):
        return self.frequency


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, string, data):
        """
        Inserts a string and returns the last node where the string ends.
        """
        node = self.root
        for char in string:
            if not node.contains_key(char):
                node.add_child(char, TrieNode())
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
            frequency = self.get(word).data[0].get_frequency()  # Assuming data[0] has frequency
            if frequency > max_freq:
                max_freq = frequency
                top_word = word

        return top_word

    @staticmethod
    def read_in_dictionary(file_name):
        """
        Reads a dictionary from a file and inserts all words into the trie.
        """
        trie = Trie()
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    try:
                        rank, word, freq = line.split()
                        rank = int(rank)
                        freq = int(freq)
                        data = TrieData(freq)
                        data.set_rank(rank)
                        trie.insert(word, data)
                    except ValueError:
                        continue  # Skip malformed lines
        except FileNotFoundError as e:
            print(f"Error: {e}")
        return trie
