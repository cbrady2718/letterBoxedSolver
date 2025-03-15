import trieClass
import time

#10X faster with pickle

t1 = time.time()
trie = trieClass.Trie()
trie = trieClass.load_trie_mmap("betterwords.pickle")
t2 = time.time()
print(t2 - t1)
t3 = time.time()
trie_two = trieClass.Trie()
trie_two = trieClass.load_trie_json("betterWords.json")
t4 = time.time()
print(t4-t3)