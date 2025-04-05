import json
import pickle
import mmap
import os


class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary to hold child nodes
        self.is_end_of_word = False  # Marks the end of a valid word

    def getChildren(self):
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
    def get_children(self,prefix):
        out = []
        node = self.root
        for char in prefix:
            print(char)
            if char not in node.children:
                return out
            node = node.children[char]
        print(node.children)
        for element in node.children:
            out.append(element)
        return out

def load_dictionary_into_trie(file_path, trie):
    """Loads all words from a dictionary file into the Trie"""
    with open(file_path, 'r') as file:
        for word in file:
            trie.insert(word.strip().lower())  # Insert words in lowercase

def load_python_list_into_trie(py_list, trie):
    for word in py_list:
        trie.insert(word.strip().lower())

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


def save_trie_pickle_mmap(trie, filename="trie.pickle"):
    """Save trie to a pickle file optimized for memory mapping"""
    with open(filename, "wb") as f:
        pickle.dump(trie, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f"Trie saved to {filename}")

def load_trie_mma2p(filename="trie.pickle"):
    """Load trie using memory mapping for instant access"""
    file_size = os.path.getsize(filename)
    
    with open(filename, "rb") as f:
        # Create memory map of the file
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        # Load the trie from the memory mapped file
        trie = pickle.load(mm)
        return trie
def load_trie_mmap(filename="trie.pickle"):
    print("Loading trie from", filename)
    
    # Explicitly import the Trie class
    import sys
    from utils.trieClass import Trie
    
    # Register the class with a compatibility name if needed
    sys.modules['trieClass'] = sys.modules['utils.trieClass']
    
    # Now load the pickle
    file_size = os.path.getsize(filename)
    with open(filename, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        trie = pickle.load(mm)
    return trie
#trie = load_trie_mmap("../betterwords.pickle")
# trie = Trie()
# dictionary_path = "/Users/chrbrady/Desktop/letterBoxApp/wordlist"
# # load_dictionary_into_trie(dictionary_path, trie)
# # save_trie_pickle_mmap(trie, "../betterwords.pickle")
# load_trie_mmap("../betterwords.pickle")
