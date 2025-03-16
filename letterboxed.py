import json
import logging
import re
import time

import requests
from bs4 import BeautifulSoup
from utils.UndirectedGraph import UndirectedGraph
from utils.nytUtil import getNYTData
import utils.trieClass as trieClass

'''print('tree loading')
new_trie = trieClass.load_trie_json('betterWords.json')
print('tree loaded')''' 

def getNYTDict():
    diction = getNYTData()
    #'ourSolution'
    trie = trieClass.Trie()
    theirSol = diction['ourSolution']
    for element in diction['dictionary']:
        trie.insert(element.lower())
    return [trie,theirSol]

nytDict = getNYTDict()
global new_trie
global nytSol
global usingNYT
usingNYT = True
new_trie, nytSol = nytDict[0], nytDict[1]
#new_trie = trieClass.load_trie_mmap("betterwords.pickle")

#new_trie = trieClass.load_trie_json('betterWords.json')

def createLetterSet(letters):
    tempSet = set()
    for element in letters:
        for let in element:
            tempSet.add(let.lower())
    return tempSet

def createletterGraph(letters):
    tempGraph = UndirectedGraph()
    for ind in range(len(letters)):
        for indy in range(len(letters[0])):
            letters[ind][indy] = letters[ind][indy].lower()
    for i in range(len(letters)-1):
        for letter in letters[i]:
            tempGraph.add_vertex(letter)
            for j in range(i+1, len(letters)):
                for l in letters[j]:
                    tempGraph.add_vertex(l)
                    tempGraph.add_edge(letter,l) 
    return tempGraph
global g
global letterSet
g = UndirectedGraph()
letterSet = set()


with open("charVals", "r") as file:
    scrabble_values = json.load(file)

def analyze(word):
    wordSet.append(word)
    score = 0
    lets = set(word)
    for element in lets:
        score += scrabble_values[element]
    byLen.append((len(word),word))
    rankedWords.append((score, word))
    byLett.append((len(lets),word))

wordSet = []

byLen = []
rankedWords = []
byLett = []

def traverse(node: trieClass.TrieNode, prfix: str):
    if len(prfix) > 2 and node.getValid():
        analyze(prfix)
    if prfix == '':
        options = g.get_vertices()
    else:
        options = g.get_neighbors(prfix[-1])
    for element in options:
        if element in node.children:
            traverse(node.children[element], prfix+element)

def solutions(word_list, chars):
    global usingNYT
    print("GETTING SOLUTIONS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    output = []
    print(usingNYT)
    if usingNYT:
        output.append([nytSol[0].lower(),nytSol[1].lower()])
    #print(word_list)
    for word in word_list:
        last = word[len(word)-1]
        matches = [w for w in word_list if w[0] == last and w!= word]
        for m in matches:
            pair = word + m
            if set(pair) == chars:
                print('found a solutions!')
                output.append([word,m])
    return output

from flask import Flask, jsonify, render_template, request

app = Flask(__name__,static_folder='.')

fuldict = {}

def getSolutions(letters):
    global new_trie
    global g
    global letterSet
    g = createletterGraph(letters)
    letterSet = createLetterSet(letters)
    traverse(new_trie.getRoot(), '')
    #print(wordSet)
    return solutions(wordSet, letterSet)

@app.route('/load_dictionary', methods=['POST'])
def run_process():
    # Get the data from the JavaScript frontend
    global new_trie
    global usingNYT
    t1 = time.time()
    new_trie = trieClass.load_trie_mmap("betterwords.pickle")
    t2 = time.time()
    print('time to load dictionary:')
    print(t2-t1)
    #new_trie = trieClass.load_trie_json('betterWords.json')
    usingNYT = False
    return jsonify("Dictionary Loaded")

@app.route('/validate', methods=['POST'])
def validate():
    # Get the data from the JavaScript frontend
    client_data = request.json
        
    # Generate the expected values
    nytDat = getNYTData()
    expected_values =  []
    for element in nytDat['sides']:
        for letter in element:
            expected_values.append(letter)
        
    # Format client data to match expected values format
    client_values = [
        client_data.get('top1', ''),
        client_data.get('top2', ''),
        client_data.get('top3', ''),
        client_data.get('left1', ''),
        client_data.get('left2', ''),
        client_data.get('left3', ''),
        client_data.get('right1', ''),
        client_data.get('right2', ''),
        client_data.get('right3', ''),
        client_data.get('bottom1', ''),
        client_data.get('bottom2', ''),
        client_data.get('bottom3', '')
    ]
    print(client_values)
    print('---------------')
    print(expected_values)
    all_match = client_values == expected_values
    global usingNYT
    if all_match:
        usingNYT = True
    print(jsonify({
        'all_match': all_match,
    }))
    return jsonify({
        'all_match': all_match,
    })

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['GET'])
def generate():
    nytDat = getNYTData()
    final =  [list(element) for element in nytDat['sides']]
    return jsonify({'letters': final})

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    top_letters = [data['top1'], data['top2'], data['top3']]
    left_letters = [data['left1'], data['left2'], data['left3']]
    right_letters = [data['right1'], data['right2'], data['right3']]
    bottom_letters = [data['bottom1'], data['bottom2'], data['bottom3']]
    
    letters = [top_letters, left_letters, right_letters, bottom_letters]
    solution = getSolutions(letters)
    byLen.sort()
    rankedWords.sort()
    byLett.sort()
    
    print(rankedWords)
    # print(byLett)
    # print(byLen)
    return jsonify({'solution': solution})

if __name__ == '__main__':
    app.run(debug=True)