import json
import logging
import re

import requests
from bs4 import BeautifulSoup

import trieClass

'''print('tree loading')
new_trie = trieClass.load_trie_json('betterWords.json')
print('tree loaded')''' 

def getNYTData():
    urlpage = 'https://www.nytimes.com/puzzles/letter-boxed'
    page = requests.get(urlpage)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page.content, 'html.parser')
    script_tag = soup.find('script', type='text/javascript', string=re.compile('window.gameData'))
    pattern = r'window\.gameData\s*=\s*({[^;]*})'
    contents = re.search(pattern, script_tag.string)
    contents = contents.group(1)
    full_data = json.loads(contents)
    print(full_data['sides'])
    return full_data

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

#new_trie = trieClass.load_trie_json('betterWords.json')
class UndirectedGraph:
    def __init__(self):
        self.graph = {}  # Dictionary to store vertices and their edges
        
    def add_vertex(self, vertex):
        """Add a vertex to the graph if it doesn't exist."""
        if vertex not in self.graph:
            self.graph[vertex] = set()
    
    def add_edge(self, vertex1, vertex2):
        """Add an undirected edge between vertex1 and vertex2."""
        # Add vertices if they don't exist
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        
        # Add edges in both directions
        self.graph[vertex1].add(vertex2)
        self.graph[vertex2].add(vertex1)
    
    def remove_edge(self, vertex1, vertex2):
        """Remove the edge between vertex1 and vertex2."""
        if vertex1 in self.graph and vertex2 in self.graph:
            self.graph[vertex1].discard(vertex2)
            self.graph[vertex2].discard(vertex1)
    
    def remove_vertex(self, vertex):
        """Remove a vertex and all its edges from the graph."""
        if vertex in self.graph:
            # Remove all edges containing this vertex
            for neighbor in self.graph[vertex]:
                self.graph[neighbor].discard(vertex)
            # Remove the vertex
            del self.graph[vertex]
    
    def get_vertices(self):
        """Return all vertices in the graph."""
        return list(self.graph.keys())
    
    def get_edges(self):
        """Return all edges in the graph as a list of tuples."""
        edges = set()
        for vertex in self.graph:
            for neighbor in self.graph[vertex]:
                # Sort the vertices to ensure we don't add the same edge twice
                edge = tuple(sorted([vertex, neighbor]))
                edges.add(edge)
        return list(edges)
    
    def get_neighbors(self, vertex):
        """Return all neighbors of a vertex."""
        if vertex in self.graph:
            return list(self.graph[vertex])
        return []
    
    def has_edge(self, vertex1, vertex2):
        """Check if an edge exists between vertex1 and vertex2."""
        return vertex1 in self.graph and vertex2 in self.graph[vertex1]
    
    def degree(self, vertex):
        """Return the degree of a vertex (number of edges connected to it)."""
        if vertex in self.graph:
            return len(self.graph[vertex])
        return 0
    
    def __str__(self):
        """Return a string representation of the graph."""
        return f"Vertices: {self.get_vertices()}\nEdges: {self.get_edges()}"
    
g = UndirectedGraph()
letterSet = set()

def createLetterSet(letters):
    #letters = [['q','s','p'],['n','l','u'],['g','a','i'],['t','h','y']]
    for ind in range(len(letters)):
        for indy in range(len(letters[0])):
            letters[ind][indy] = letters[ind][indy].lower()
    for i in range(len(letters)-1):
        for letter in letters[i]:
            g.add_vertex(letter)
            for j in range(i+1, len(letters)):
                for l in letters[j]:
                    g.add_vertex(l)
                    g.add_edge(letter,l)
    for element in letters:
        for let in element:
            letterSet.add(let.lower())


with open("charVals", "r") as file:
    scrabble_values = json.load(file)

def analyze(word):
    wordSet.append(word)
    score = 0
    lets = set(word)
    for element in lets:
        score += scrabble_values[element]
    rankedWords.append((score, word))

wordSet = []

rankedWords = []

def traverse(node: trieClass.TrieNode, prfix: str):
    if len(prfix) > 1 and node.getValid():
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
                output.append([word,m])
    return output

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

fuldict = {}

def getSolutions(letters):
    global new_trie
    createLetterSet(letters)
    traverse(new_trie.getRoot(), '')
    #print(wordSet)
    return solutions(wordSet, letterSet)

@app.route('/load_dictionary', methods=['POST'])
def run_process():
    # Get the data from the JavaScript frontend
    global new_trie
    global usingNYT
    new_trie = trieClass.load_trie_mmap("betterwords.pickle")
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
    rankedWords.sort()
    #print(rankedWords)
    return jsonify({'solution': solution})

if __name__ == '__main__':
    app.run(debug=True)