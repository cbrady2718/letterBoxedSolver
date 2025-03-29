import json
import logging
import re
import time

import os
import requests
from bs4 import BeautifulSoup
from utils.UndirectedGraph import UndirectedGraph
from utils.GetDictionary import getNYTData
import utils.trieClass as trieClass
from utils.trieClass import Trie
from utils.trieClass import TrieNode
from utils.trieClass import load_trie_mmap
import utils.GetDictionary as GetDictionary
import utils.Solver as Solver




def updateHistory():
    with open("Dictionary/past_solutions.json", 'r') as file:
        data = json.load(file)
    file.close()
    today = GetDictionary.getNYTData()
    date = today['printDate']
    if date not in data.keys():
        print(f"processing {date}")
        sides = today['sides']
        prefSol = today['ourSolution']
        outWords = today['dictionary']
        print("loading nyt trie...")
        trie = trieClass.load_trie_mmap("Dictionary/nyt_dict.pickle")
        print("adding today's words")
        trieClass.load_python_list_into_trie(outWords, trie)
        print("saving dict")
        trieClass.save_trie_pickle_mmap(trie, "Dictionary/nyt_dict.pickle")

        subOutDict = {"sides" : sides, "sol" : prefSol}
        data[date] =subOutDict
        print(f"saving dict {data}")
        with open('Dictionary/past_solutions.json', 'w') as fp:
            json.dump(data, fp)
        fp.close()
        print("processing complete")
    else:
        print(f"already processed {date}")
