class TrieNode:
    def __init__(self):
        """
        Initializes a TrieNode with a dictionary to hold children,
        a boolean to mark the end of a word, and a list to hold data.
        """
        self.children = {}  # Dictionary to store child TrieNodes
        self.is_end = False  # Marks if this node is the end of a word
        self.data = []  # List to store associated data for this node

    def contains_key(self, char):
        """
        Checks if the current node contains a child node for the given character.
        :param char: The character to check for.  
        :return: True if the character is in the children, False otherwise.
        """
        return char in self.children

    def add_child(self, char, node):
        """
        Adds a child node for the given character.
        :param char: The character for the child node.
        :param node: The TrieNode to add as a child.
        """
        self.children[char] = node

    def get_child(self, char):
        """
        Retrieves the child node for the given character.
        :param char: The character whose child node is to be retrieved.
        :return: The TrieNode corresponding to the character, or None if not found.
        """
        return self.children.get(char)

    def add_data(self, data):
        """
        Adds data to this node's data list.
        :param data: The data to add.
        """
        self.data.append(data)

    def set_end(self):
        """
        Marks this node as the end of a word.
        """
        self.is_end = True

    def is_end_node(self):
        """
        Checks if this node marks the end of a word.
        :return: True if this node is the end of a word, False otherwise.
        """
        return self.is_end
