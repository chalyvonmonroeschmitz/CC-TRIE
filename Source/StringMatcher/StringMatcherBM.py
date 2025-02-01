class StringMatcherBM:
    """
    A class that implements the Boyer-Moore string matching algorithm.
    """

    def __init__(self):
        pass

    def boyer_moore_match(self, text, pattern):
        """
        Implements the Boyer-Moore string matching algorithm.
        Returns a list of starting indices where the pattern occurs in the text.

        :param text: The main text to search in.
        :param pattern: The pattern to search for within the text.
        :return: A list of indices where the pattern is found in the text.
        """
        if pattern == "":
            return []  # No pattern provided to search

        text_length = len(text)
        pattern_length = len(pattern)

        if pattern_length > text_length:
            return []  # No match possible if the pattern is longer than the text

        # Preprocessing step: Create the bad character heuristic
        bad_char_shift = self._preprocess_bad_character(pattern)

        matches = []
        shift = 0  # Starting position in the text

        # Perform matching
        while shift <= (text_length - pattern_length):
            j = pattern_length - 1

            # Compare from the end of the pattern to the beginning
            while j >= 0 and pattern[j] == text[shift + j]:
                j -= 1

            # If the pattern is fully matched
            if j < 0:
                matches.append(shift)
                shift += (pattern_length - bad_char_shift[ord(text[shift + pattern_length])]
                          if shift + pattern_length < text_length else 1)
            else:
                # Shift according to the bad character heuristic
                shift += max(1, j - bad_char_shift[ord(text[shift + j])])

        return matches

    def _preprocess_bad_character(self, pattern):
        """
        Preprocesses the bad character heuristic table for Boyer-Moore.

        This table determines how far the pattern should be shifted when a mismatch occurs.

        :param pattern: The pattern for which the bad character heuristic is computed.
        :return: An array of size 256 (ASCII chars), where each entry specifies the shift length for mismatched characters.
        """
        bad_char_shift = [-1] * 256  # Default value for all characters is -1

        for i in range(len(pattern)):
            bad_char_shift[ord(pattern[i])] = i  # Index of the last occurrence of the character in the pattern

        return bad_char_shift

def main():
    """
    Main function to test the StringMatcherBM class.
    """
    text = input("Enter the text: ").strip()
    pattern = input("Enter the pattern to search for: ").strip()
    matcher = StringMatcherBM()

    print("\nBoyer-Moore String Matching")
    matches = matcher.boyer_moore_match(text, pattern)
    if matches:
        print(f"Pattern found at indices: {matches}")
    else:
        print("Pattern not found.")


if __name__ == "__main__":
    main()
