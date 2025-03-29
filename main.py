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

'''print('tree loading')
new_trie = trieClass.load_trie_json('betterWords.json')
print('tree loaded')''' 

global active_trie
global isNYT
global recommendedSol
metaDat = GetDictionary.getDict(True)
active_trie = metaDat["trie"]
isNYT = metaDat["isNYT"]
recommendedSol = ""
if isNYT:
    recommendedSol = metaDat["solution"]


global g
global letterSet
g = UndirectedGraph()
letterSet = set()

from flask import Flask, jsonify, render_template, request

app = Flask(__name__,static_folder='.')


@app.route('/load_dictionary', methods=['POST'])
def run_process():
    print('entered py')
    global active_trie
    global isNYT
    global recommendedSol
    
    # Get the boolean parameter from the request
    data = request.get_json()
    use_nyt = data.get('useNYT', False)  # Default to False if not provided
    
    dict_dict = GetDictionary.getDict(use_nyt)
    # print("-----------")
    # print("printing dict_dict")
    # print(dict_dict)
    # print("---------")
    active_trie = dict_dict["trie"]
    isNYT = dict_dict["isNYT"]
    recommendedSol = dict_dict["solution"]
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
    # print(client_values)
    # print('---------------')
    # print(expected_values)
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
    global recommendedSol
    global active_trie
    global isNYT
    data = request.get_json()
    top_letters = [data['top1'], data['top2'], data['top3']]
    left_letters = [data['left1'], data['left2'], data['left3']]
    right_letters = [data['right1'], data['right2'], data['right3']]
    bottom_letters = [data['bottom1'], data['bottom2'], data['bottom3']]
    
    letters = [top_letters, left_letters, right_letters, bottom_letters]
    # print(letters)
    # print(recommendedSol)
    # print(isNYT)
    solution = Solver.getSolutions(letters, active_trie, recommendedSol)

    return jsonify({'solution': solution})


if __name__ == "__main__":
    app.run()
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host="0.0.0.0", port=port)