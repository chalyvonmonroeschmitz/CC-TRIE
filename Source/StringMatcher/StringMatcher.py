class StringMatcher:
    """
    A class for string matching using different algorithms such as Naive, KMP, and Rabin-Karp.
    """

    def __init__(self):
        pass

    def naive_match(self, text, pattern):
        """
        Implements the Naive String Matching algorithm.
        Returns the starting indices of all occurrences of the pattern in the text.
        """
        text_length = len(text)
        pattern_length = len(pattern)
        matches = []

        for i in range(text_length - pattern_length + 1):
            match_found = True
            for j in range(pattern_length):
                if text[i + j] != pattern[j]:
                    match_found = False
                    break
            if match_found:
                matches.append(i)

        return matches

    def kmp_match(self, text, pattern):
        """
        Implements the Knuth-Morris-Pratt (KMP) algorithm for pattern matching.
        Returns the starting indices of all occurrences of the pattern in the text.
        """
        def build_lps(pattern):
            """
            Builds the Longest Prefix Suffix (LPS) array for the KMP algorithm.
            """
            lps = [0] * len(pattern)
            length = 0  # Length of the previous longest prefix suffix
            i = 1

            while i < len(pattern):
                if pattern[i] == pattern[length]:
                    length += 1
                    lps[i] = length
                    i += 1
                else:
                    if length != 0:
                        length = lps[length - 1]
                    else:
                        lps[i] = 0
                        i += 1

            return lps

        text_length = len(text)
        pattern_length = len(pattern)
        lps = build_lps(pattern)
        matches = []
        i = 0  # Index in text
        j = 0  # Index in pattern

        while i < text_length:
            if pattern[j] == text[i]:
                i += 1
                j += 1

            if j == pattern_length:
                matches.append(i - j)
                j = lps[j - 1]
            elif i < text_length and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1

        return matches

    def rabin_karp_match(self, text, pattern, prime=101):
        """
        Implements the Rabin-Karp algorithm
        """

def main():
    """
    Main function to test the StringMatcherBF class.
    """
    text_file = open("Data/Frank.txt", 'r')

    text = [text_file.read().strip()]
    pattern = input("Enter the pattern to search for: ").strip()
    matcher = StringMatcher()

    print("\nBrute Force String Matching")
    matches = matcher.naive_match(text[0], pattern)
    print(f"Indices where pattern occurs: {matches}")

if __name__ == "__main__":
    main()
