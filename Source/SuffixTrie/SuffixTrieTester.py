from SuffixTrie import SuffixTrie

def main():
    """
    Main function to test the enhanced SuffixTrie with metadata (SuffixTrieData).
    """
    # Create an empty Suffix Trie
    suffix_trie = SuffixTrie()

    # Load content from the file into the trie
    suffix_trie.load_from_file("Data/Frank.txt")

    # Check the contents of the loaded text
    print("Text:", suffix_trie.text)

    while True:
        print("\nOptions:")
        print("1. Check if a pattern exists in the Suffix Trie")
        print("2. Get metadata (positions and frequency) for a suffix/pattern")
        print("3. Get all suffixes with a given prefix")
        print("4. Exit")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            pattern = input("Enter the pattern to search for: ").strip()
            if suffix_trie.contains(pattern):
                print("Pattern exists in the Suffix Trie.")
            else:
                print("Pattern does not exist in the Suffix Trie.")
        elif choice == 2:
            pattern = input("Enter the pattern to get metadata for: ").strip()
            metadata = suffix_trie.get_suffix_metadata(pattern)
            if metadata:
                print(f"Metadata for '{pattern}': {metadata}")
            else:
                print(f"No metadata found for '{pattern}'.")
        elif choice == 3:
            prefix = input("Enter the prefix: ").strip()
            suffixes = suffix_trie.get_suffixes_with_prefix(prefix)
            print(f"Suffixes starting with '{prefix}': ")
            i = 0
            for suffix in suffixes:
                i += 1
                print(f"{i}) {suffix}")

        elif choice == 4:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
