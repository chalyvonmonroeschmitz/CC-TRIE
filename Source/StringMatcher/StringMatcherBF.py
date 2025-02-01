class StringMatcherBF:
    """
    A string matcher that implements the Brute Force algorithm for substring searching.
    """

    def __init__(self):
        pass

    def brute_force_match(self, text, pattern):
        """
        Implements the Brute Force string matching algorithm.
        Returns a list of starting indices where the pattern occurs in the text.

        :param text: The main text to search in.
        :param pattern: The pattern to search for within the text.
        :return: A list of indices where the pattern is found in the text.
        """
        text_length = len(text)
        pattern_length = len(pattern)
        matches = []

        # Slide over the text one character at a time
        for i in range(text_length - pattern_length + 1):
            match_found = True

            # Compare characters of text and pattern one by one
            for j in range(pattern_length):
                if text[i + j] != pattern[j]:
                    match_found = False
                    break

            if match_found:
                matches.append(i)

        return matches

def main():
    """
    Main function to test the StringMatcherBF class.
    """
    text = input("Enter the text: ").strip()
    pattern = input("Enter the pattern to search for: ").strip()
    matcher = StringMatcherBF()

    print("\nBrute Force String Matching")
    matches = matcher.brute_force_match(text, pattern)
    print(f"Indices where pattern occurs: {matches}")


if __name__ == "__main__":
    main()
