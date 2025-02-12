from StringMatcherBF import StringMatcherBF
from StringMatcherBM import StringMatcherBM
from StringMatcherKMP import StringMatcherKMP


def main():
    """
    Main function to test the StringMatcherBF class.
    """
    smbf = StringMatcherBF()
    smBM = StringMatcherBM()
    smKMP = StringMatcherKMP()

    text_file = open("Data/Frankenstein.txt", 'r')

    text = [text_file.read().strip()]
    print(text[:])
    pattern = input("Enter the pattern to search for: ").strip()

    print("\nBrute Force String Matching")
    matches = smBM.boyer_moore_match(text[0], pattern)
    print(f"Indices where pattern occurs: {matches}")

if __name__ == "__main__":
    main()
