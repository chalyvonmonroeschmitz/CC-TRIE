from SuffixTrieNode import SuffixTrieNode
import sys
# increase the default recursion limit for larger branch sizing
sys.setrecursionlimit(10**4) # 10 power 4

class SuffixTrie:
    """
    Implementation of a SuffixTrie to store all suffixes of a string.
    Now supports metadata through SuffixTrieData (e.g., positions, frequency).
    """

    def __init__(self, text=None):
        """
        Initializes the Suffix Trie with a given string and constructs the trie.
        """
        self.text = text
        self.root = SuffixTrieNode()

        # Add all suffixes of the given text to the trie
        if text:
            for i in range(len(text)):
                suffix = text[i:]
                self._insert(suffix, i)

    def _insert(self, suffix, start_position):
        """
        Inserts a suffix into the Suffix Trie.
        Also records metadata such as the starting position and frequency.
        """
        node = self.root
        for char in suffix:
            node.add_child(char)
            node = node.get_child(char)
            node.data.increment_frequency()  # Update frequency for traversed nodes
            node.data.add_position(start_position)

        # Mark the last node as terminal and add position metadata
        node.is_terminal = True

    def load_from_file(self, file_path):
        """
        Reads a text file and builds a Suffix Trie from its contents.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.text = file.read().strip()  # Read all text and strip extra whitespace

            # Clear existing trie and construct the new one
            self.root = SuffixTrieNode()
            for i in range(len(self.text)):
                suffix = self.text[i:]
                self._insert(suffix, i)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    def contains(self, pattern):
        """
        Checks if a pattern exists in the Suffix Trie.
        """
        node = self.root
        for char in pattern:
            node = node.get_child(char)
            if node is None:
                return False
        return True

    def get_suffix_metadata(self, pattern):
        """
        Retrieves metadata (SuffixTrieData) for the given suffix/pattern.
        Returns None if the pattern doesn't exist.
        """
        node = self.root
        for char in pattern:
            node = node.get_child(char)
            if node is None:
                return None
        return node.data

    def get_suffixes_with_prefix(self, prefix):
        """
        Returns a list of all suffixes that start with a given prefix.
        """
        node = self.root
        for char in prefix:
            node = node.get_child(char)
            if node is None:
                return []  # If the prefix doesn't exist, return an empty list

        suffixes = []
        self._collect_suffixes(node, prefix, suffixes)
        return suffixes

    def _collect_suffixes(self, node, current_suffix, suffixes):
        """
        Recursively collects all suffixes starting from the given node.
        """
        if node.is_terminal:
            suffixes.append(current_suffix)

        for char, child_node in node.children.items():
            self._collect_suffixes(child_node, current_suffix + char, suffixes)

    def __str__(self):
        """
        String representation of the Suffix Trie for debugging.
        """
        suffixes = []
        self._collect_suffixes(self.root, "", suffixes)
        return "\n".join(suffixes)
