import json
import logging
import re
import time
import WordPuzzleHintEngine

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

'''print('tree loading')
new_trie = trieClass.load_trie_json('betterWords.json')
print('tree loaded')''' 
global small_trie
global large_trie
global using_small

global recommendedSol
global current_dictionary
recommendedSol = ""
current_dictionary = {}
current_date = ''
metaDat = GetDictionary.getDict(True)
#automatically set small trie to todays trie
small_trie = Trie()
#automatically load large_trie
large_trie = GetDictionary.getDict(False)['trie']
#defaul will assume today's trie
using_small = False



global g
global letterSet
g = UndirectedGraph()
letterSet = set()

from flask import Flask, jsonify, render_template, request

app = Flask(__name__,static_folder='.')


@app.route('/load_dictionary', methods=['POST'])
def run_process():
    return jsonify("Don't need this")

@app.route('/validate', methods=['POST'])
def validate():
    # Get the data from the JavaScript frontend
    global current_dictionary
    global using_small

    client_data = request.json
        
    nytDat = current_dictionary
    if 'sides' not in nytDat:
        using_small = False
        return jsonify({
            'all_match': False,
        })
    # Generate the expected values
    #nytDat = getNYTData()
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

    all_match = client_values == expected_values
    if all_match and 'dictionary' in nytDat:
        using_small = True
    else:
        using_small = False
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

@app.route('/get_dates')
def get_dates():
    with open('nyt_data.json', 'r') as f:
        dates_data = json.load(f)
        bob = dates_data.keys()
    return jsonify(dates_data)

def processDate(date):
    global small_trie
    global using_small
    global large_trie
    global current_dictionary
    with open('nyt_data.json', 'r') as f:
        dates_data = json.load(f)
        final =  [list(element) for element in dates_data[date]['sides']]
        current_dictionary = dates_data[date]
        print(dates_data[date].keys())
        if "dictionary" in dates_data[date]:
            print("using new dictionary")
            small_trie = Trie()
            trieClass.load_python_list_into_trie(dates_data[date]["dictionary"], small_trie)
            using_small = True
        else:
            print("not using small")
            if "outSolution" in dates_data[date]:
                for element in dates_data[date]["outSolution"]:
                    large_trie.insert(element)
            using_small = False
        return final

@app.route('/process_date', methods=['POST'])
def process_date():
    print('hi')
    print(request)
    data = request.json
    print(data)
    selected_date = data.get('date')
    sides = processDate(selected_date)
    return jsonify({'letters': sides})


@app.route('/validate_word', methods=['POST'])  
def checkWord():
    word = request.get_json().get("word")
    word = word.lower()
    print(word)
    print(using_small)
    if using_small:
        test = small_trie.search(word)
    else:
        test = large_trie.search(word)

    return jsonify({
        'valid': test
    })


@app.route('/hint', methods=['POST'])
def hint():
    print("IM IN THE HINT")
    global using_small
    global small_trie
    global large_trie
    global current_dictionary

    global recommendedSol
    data = request.get_json()
    print(data)
    top_letters = [data['top1'], data['top2'], data['top3']]
    left_letters = [data['left1'], data['left2'], data['left3']]
    right_letters = [data['right1'], data['right2'], data['right3']]
    bottom_letters = [data['bottom1'], data['bottom2'], data['bottom3']]
    
    letters = [top_letters, left_letters, right_letters, bottom_letters]
    prefix = data['cur'].lower()
    outHint = []
    if using_small:
        recommendedSol = current_dictionary['outSolution']
        if "dictionary" in current_dictionary:
            outHint = small_trie.get_children(prefix)
        else:
            outHint = large_trie.get_children(prefix)
    else:
        outHint = large_trie.get_children(prefix)
    print(outHint)
    return jsonify({'hint': outHint})

@app.route('/solve', methods=['POST'])
def solve():
    global using_small
    global small_trie
    global large_trie
    global current_dictionary

    global recommendedSol
    data = request.get_json()
    top_letters = [data['top1'], data['top2'], data['top3']]
    left_letters = [data['left1'], data['left2'], data['left3']]
    right_letters = [data['right1'], data['right2'], data['right3']]
    bottom_letters = [data['bottom1'], data['bottom2'], data['bottom3']]
    
    letters = [top_letters, left_letters, right_letters, bottom_letters]
    if using_small:
        recommendedSol = current_dictionary['outSolution']
        if "dictionary" in current_dictionary:
            solution = Solver.getSolutions(letters, small_trie, recommendedSol)
        else:
            solution = Solver.getSolutions(letters, large_trie, recommendedSol)
    else:
        solution = Solver.getSolutions(letters, large_trie, "")
    return jsonify({'solution': solution})


if __name__ == "__main__":
    app.run()
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host="0.0.0.0", port=port)