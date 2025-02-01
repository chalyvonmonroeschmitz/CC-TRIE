class SuffixTrieData:
    """
    Class to represent metadata for suffixes stored in the Suffix Trie.
    Stores position(s) of the suffix in the original string and other optional data.
    """

    def __init__(self):
        self.positions = []  # List to store all positions where the suffix occurs
        self.frequency = 0  # Frequency count (if applicable)

    def add_position(self, position):
        """
        Adds a position for the suffix in the original string.
        """
        self.positions.append(position)

    def increment_frequency(self):
        """
        Increases the frequency count for this suffix.
        Useful in cases where we're counting occurrences of substrings.
        """
        self.frequency += 1

    def get_positions(self):
        """
        Returns all positions for the suffix in the original string.
        """
        return self.positions

    def get_frequency(self):
        """
        Returns the frequency of occurrences of the suffix.
        """
        return self.frequency

    def __str__(self):
        """
        String representation of the SuffixTrieData object.
        """
        return f"SuffixTrieData(positions={self.positions}, frequency={self.frequency})"
