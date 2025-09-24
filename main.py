import json


import os
import time
from bs4 import BeautifulSoup
from utils.UndirectedGraph import UndirectedGraph
from utils.GetDictionary import getNYTData
import utils.trieClass as trieClass
from utils.trieClass import Trie
from utils.trieClass import TrieNode
from utils.trieClass import load_trie_mmap
import utils.GetDictionary as GetDictionary
import utils.Solver as Solver
import utils.gridGenerator as gridGenerator


from flask import Flask, jsonify, render_template, request

app = Flask(__name__,static_folder='.')
global large_trie
large_trie = GetDictionary.getDict(False)['trie']

def processDate(date):
    global large_trie
    outDict = {}
    with open('nyt_data.json', 'r') as f:
        dates_data = json.load(f)
        final =  [list(element) for element in dates_data[date]['sides']]
        print(dates_data[date].keys())
        if "dictionary" in dates_data[date]:
            print("using new dictionary")
            small_trie = Trie()
            trieClass.load_python_list_into_trie(dates_data[date]["dictionary"], small_trie)
            outDict = small_trie.trie_to_dict()
        else:
            print('starting timer')
            t1 = time.time()
            if "outSolution" in dates_data[date]:
                for element in dates_data[date]["outSolution"]:
                    large_trie.insert(element)
            outTrie = large_trie.trim_trie_to_grid(final)
            outDict = outTrie.trie_to_dict()
            t2 = time.time()
            print("Elapsed time:", t2 - t1, "seconds")
        return {"sides" : final, "trie" : outDict, "solution" : dates_data[date]["outSolution"]}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_dates')
def get_dates():
    with open('nyt_data.json', 'r') as f:
        dates_data = json.load(f)
        bob = dates_data.keys()
    return jsonify(dates_data)

@app.route('/get_puzzle_data', methods=['POST'])
def get_puzzle_data():
    req = request.get_json()
    date = req['date']
    returnDict = processDate(date)
    print("returning", returnDict.keys())
    sides = returnDict['sides']
    trie = returnDict['trie'] 
    solution = returnDict['solution']

    # Generate sides, solution, trie for the given date
    return jsonify({
        "sides": sides,
        "trie": trie,
        "solution":  solution
    })

@app.route('/generate_grid', methods=['GET'])
def generate_grid():
    global large_trie
    print('in here!!!')
    res = gridGenerator.generateGrid()
    print("finished generating")
    print(res)
    print("------------")
    sides = res[0]
    solution = res[1]
    outTrie = large_trie.trim_trie_to_grid(sides)
    outDict = outTrie.trie_to_dict()
    return jsonify({'sides': sides, 'trie': outDict, 'solution': solution})

@app.route('/solve_puzzle', methods=['POST'])
def solve():
    print('we have entered!')
    data = request.get_json()
    jsTree = data['trie']
    pyTree = Trie()
    t1 = time.time()
    pyTree.dict_to_trie(jsTree)
    t2 = time.time()
    print("Time to rebuild tree:", t2 - t1, "seconds")
    top_letters = [data['top1'], data['top2'], data['top3']]
    left_letters = [data['left1'], data['left2'], data['left3']]
    right_letters = [data['right1'], data['right2'], data['right3']]
    bottom_letters = [data['bottom1'], data['bottom2'], data['bottom3']]
    
    letters = [top_letters, left_letters, right_letters, bottom_letters]
    t3 = time.time()
    solution = Solver.getSolutions(letters, pyTree)
    t4 = time.time()
    print("Time to solve:", t4 - t3, "seconds")
    return jsonify({'solution': solution})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    #app.run()
