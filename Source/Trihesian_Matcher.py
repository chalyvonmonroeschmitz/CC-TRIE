import sys
from Trie import Trie
import math
import re
from google_scraper import Google_Scraper


def Get_Cohesion_Constant(compound_d, compound_i, compound_h):
    # (3 * ((d1 + d2 + d3) + (i1 + i2 + i3) + (h1 + h2 + h3)) + 50) * Reciprical of Pi / 1000
    cohesion_constant =  (3 * sum(compound_d.values()) + sum(compound_i.values()) + sum(compound_h.values()) + 50) * math.pi / 10000
    return cohesion_constant

def Get_Mass(compound):
    # Regular expression to match elements and their quantities
    pattern = re.compile(r'([A-Z][a-z]*)(\d*)')
    matches = pattern.findall(compound)

    elements_dict = {}
    for (element, quantity) in matches:
        if quantity == '':
            quantity = 1
        else:
            quantity = int(quantity)
        if element in elements_dict:
            elements_dict[element] += quantity
        else:
            elements_dict[element] = quantity
    return elements_dict

def main():
    # Initialize the Trie
    trie = Trie()
    google_scraper = Google_Scraper()
    search = ""
    region = ""
    command = sys.argv

    if len(sys.argv) > 0:
        for i, c in enumerate(command):
            if "--search" in c:
                search = command[i + 1]
            if "--region" in c:
                region = command[i + 1]
    google_scraper.google_scraper(google_scraper, search, region)

    # Load element data from file (Update file path accordingly)
    file_name = "../Data/elements_table_v20.txt"
    try:
        trie = trie.read_in_dictionary(file_name)
    except FileNotFoundError:
        print(f"File {file_name} not found. Please provide a valid file path.")

    compound_d = Get_Mass("aCO3+6H2O")
    compound_i = Get_Mass("aCO3+6H2O")
    compound_h = Get_Mass("aCO3+6H2O")
    print(Get_Cohesion_Constant(compound_d, compound_i, compound_h))

def load_chrome_scraper():
    datacaptures = []
    scraper = Google_Scraper()
    driver = scraper.initChromeDriver(True)
    return driver

def Graph_Compound_Tree():
    compounds = []

# Call the main function to run the tests
if __name__ == "__main__":
    main()
