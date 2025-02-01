from SuffixTrieData import SuffixTrieData

class SuffixTrieNode:
    """
    Represents a node in the Suffix Trie.
    Each node contains children for every character, a flag indicating terminal nodes,
    and metadata (`SuffixTrieData`) for suffix-related information.
    """

    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.is_terminal = False  # Indicates the end of a suffix
        self.data = SuffixTrieData()  # Metadata for this node (e.g., positions)

    def add_child(self, char):
        """
        Add a child node for a given character if it doesn't already exist.
        """
        if char not in self.children:
            self.children[char] = SuffixTrieNode()

    def get_child(self, char):
        """
        Gets the child node for a given character, or None if it doesn't exist.
        """
        return self.children.get(char)

    def __str__(self):
        """
        String representation of the node for debugging purposes.
        """
        return f"SuffixTrieNode(children={list(self.children.keys())}, is_terminal={self.is_terminal}, data={self.data})"
