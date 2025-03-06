import json


class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary to hold child nodes
        self.is_end_of_word = False  # Marks the end of a valid word

    def getChildren(self):
        for element in self.children:
            print(element)
        print('--------')
        return self.children
    
    def getValid(self):
        return self.is_end_of_word

class Trie:
    def __init__(self):
        self.root = TrieNode()  # Root node of the Trie

    def getRoot(self):
        return self.root

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True  # Marks the word as complete

    def search(self, word):
        """Returns True if word is in Trie, else False"""
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        """Returns True if any word in Trie starts with given prefix"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

def load_dictionary_into_trie(file_path, trie):
    """Loads all words from a dictionary file into the Trie"""
    with open(file_path, 'r') as file:
        for word in file:
            trie.insert(word.strip().lower())  # Insert words in lowercase



def trie_to_dict(node):
    """Recursively convert TrieNode to a dictionary"""
    return {
        'children': {char: trie_to_dict(child) for char, child in node.children.items()},
        'is_end_of_word': node.is_end_of_word
    }

def save_trie_json(trie, filename="trie.json"):
    """Save the Trie to a JSON file"""
    with open(filename, "w") as file:
        json.dump(trie_to_dict(trie.root), file)
    print(f"Trie saved to {filename}")

def dict_to_trie(node_dict):
    """Recursively convert dictionary back to TrieNode"""
    node = TrieNode()
    node.is_end_of_word = node_dict.get('is_end_of_word', False)
    for char, child_dict in node_dict.get('children', {}).items():
        node.children[char] = dict_to_trie(child_dict)
    return node

def load_trie_json(filename="trie.json"):
    """Load Trie from a JSON file"""
    with open(filename, "r") as file:
        node_dict = json.load(file)
    trie = Trie()
    trie.root = dict_to_trie(node_dict)
    return trie
'''# Example Usage
trie = Trie()
#dictionary_path = "/Users/chrbrady/nltk_data/corpora/words/en"  # Standard dictionary file path on Linux/macOS
#dictionary_path = "/Users/chrbrady/Downloads/words_alpha.txt"
dictionary_path = "/Users/chrbrady/Desktop/letterBoxApp/wordlist"
load_dictionary_into_trie(dictionary_path, trie)

save_trie_json(trie, 'michWords.json')
'''