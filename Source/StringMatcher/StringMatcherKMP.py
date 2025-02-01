class StringMatcherKMP:
    """
    A class that implements the Knuth-Morris-Pratt (KMP) algorithm for efficient string matching.
    """

    def __init__(self):
        pass

    def kmp_match(self, text, pattern):
        """
        Implements the KMP string matching algorithm.
        Returns a list of starting indices where the pattern occurs in the text.

        :param text: The main text to search in.
        :param pattern: The pattern to search for within the text.
        :return: A list of indices where the pattern is found in the text.
        """
        if not pattern or not text:
            return []  # Return empty if pattern or text is missing

        n = len(text)
        m = len(pattern)
        lps = self._compute_lps(pattern)  # Preprocess the pattern
        matches = []

        i = 0  # Index for text
        j = 0  # Index for pattern

        while i < n:
            if text[i] == pattern[j]:  # Characters match
                i += 1
                j += 1

            if j == m:  # Full pattern match
                matches.append(i - j)  # Add the starting index of the match
                j = lps[j - 1]  # Reset j to check for overlapping matches
            elif i < n and text[i] != pattern[j]:  # Mismatch after j matches
                if j != 0:
                    j = lps[j - 1]  # Use the LPS array to avoid rechecking
                else:
                    i += 1  # Move to the next character in text

        return matches

    def _compute_lps(self, pattern):
        """
        Computes the Longest Prefix Suffix (LPS) array for the pattern.

        The LPS array is used to determine how much to shift the pattern in the event of a mismatch.

        :param pattern: The pattern to preprocess.
        :return: A list representing the LPS array.
        """
        m = len(pattern)
        lps = [0] * m
        length = 0  # Length of the previous longest prefix suffix
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]  # Fall back to the previous LPS position
                else:
                    lps[i] = 0
                    i += 1

        return lps

class StringMatcher:
    """
    Unified interface for different string matching algorithms.
    """

    def __init__(self):
        self.kmp = StringMatcherKMP()
        # Add other algorithms like Boyer-Moore, etc., if needed.

    def kmp_match(self, text, pattern):
        return self.kmp.kmp_match(text, pattern)

    # Add other methods (e.g., boyer_moore_match) if needed here.

def main():
    """
    Main function to test the StringMatcherKMP class.
    """
    text = input("Enter the text: ").strip()
    pattern = input("Enter the pattern to search for: ").strip()
    matcher = StringMatcherKMP()

    print("\nKnuth-Morris-Pratt (KMP) String Matching")
    matches = matcher.kmp_match(text, pattern)
    if matches:
        print(f"Pattern found at indices: {matches}")
    else:
        print("Pattern not found.")


if __name__ == "__main__":
    main()
