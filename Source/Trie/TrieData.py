class TrieData:
    def __init__(self, frequency):
        """
        Initializes an instance of TrieData with a frequency and rank.
        :param frequency: The frequency associated with the word.
        """
        self.frequency = frequency  # Frequency of the word
        self.rank = None  # Rank of the word

    def set_rank(self, rank):
        """
        Sets the rank for this TrieData instance.
        :param rank: The rank to set.
        """
        self.rank = rank

    def get_rank(self):
        """
        Retrieves the rank of this TrieData instance.
        :return: The rank of the word.
        """
        return self.rank

    def get_frequency(self):
        """
        Retrieves the frequency of this TrieData instance.
        :return: The frequency of the word.
        """
        return self.frequency
