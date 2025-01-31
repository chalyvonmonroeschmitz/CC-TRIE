from Trie import Trie, TrieNode, TrieData

def main():
    # Initialize the Trie
    trie = Trie()

    # 1. Insert Strings into the Trie
    print("Inserting words into the trie...")
    first_data = TrieData(10)  # Example: word with frequency 10
    first_data.set_rank(1)
    trie.insert("apple", first_data)

    second_data = TrieData(15)  # Example: word with frequency 15
    second_data.set_rank(2)
    trie.insert("ape", second_data)

    third_data = TrieData(5)  # Example: word with frequency 5
    third_data.set_rank(3)
    trie.insert("bat", third_data)

    fourth_data = TrieData(7)
    fourth_data.set_rank(4)
    trie.insert("ball", fourth_data)

    print("Words inserted!")

    # 2. Test `get` Method
    print("\nTesting the `get` method...")
    result = trie.get("apple")
    if result:
        print(f"Successfully found word 'apple' with frequency: {result.data[0].get_frequency()}")
    else:
        print("Word 'apple' not found!")

    result = trie.get("bat")
    if result:
        print(f"Successfully found word 'bat' with frequency: {result.data[0].get_frequency()}")
    else:
        print("Word 'bat' not found!")

    # 3. Test `get_alphabetical_list_with_prefix`
    print("\nTesting `get_alphabetical_list_with_prefix`...")
    prefix = "a"
    words_with_prefix = trie.get_alphabetical_list_with_prefix(prefix)
    print(f"Words with prefix '{prefix}': {words_with_prefix}")

    # 4. Test `get_words` Method
    print("\nTesting `get_words` method...")
    all_words = trie.get_words()
    print(f"All words in the trie: {all_words}")

    # 5. Test `get_most_frequent_word_with_prefix`
    print("\nTesting the `get_most_frequent_word_with_prefix` method...")
    prefix = "a"
    most_frequent_word = trie.get_most_frequent_word_with_prefix(prefix)
    if most_frequent_word:
        print(f"The most frequent word with prefix '{prefix}' is: {most_frequent_word}")
    else:
        print(f"No words found with prefix '{prefix}'.")

    # 6. Test `read_in_dictionary` Method (Optional depending on input file)
    print("\nTesting `read_in_dictionary` method...")
    file_name = "Data/word-freq-grow.txt"  # Update to the path of the dictionary file, if available
    try:
        dictionary_trie = Trie.read_in_dictionary(file_name)
        print(f"Dictionary loaded successfully from {file_name}!")
        print("Words in the dictionary:", dictionary_trie.get_words())
    except FileNotFoundError:
        print(f"File {file_name} not found. Skipping this test.")

    print("\nAll tests completed!")


# Call the main function to run the tests
if __name__ == "__main__":
    main()
