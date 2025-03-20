import utils.trieClass as trieClass
import utils.GetDictionary as GetDictionary
import json

global wordSet
wordSet = []

def analyze(word, scrabble_values):
    wordSet.append(word)
    score = 0
    lets = set(word)
    for element in lets:
        score += scrabble_values[element]
    scrabble_score = score
    length_score = len(word)
    letter_score = len(lets)
    return(scrabble_score, length_score, letter_score)

def traverse(node: trieClass.TrieNode, prfix: str, letterGraph: GetDictionary.UndirectedGraph):
    if prfix == '':
        print(letterGraph.get_vertices())
    global wordSet
    if len(prfix) > 2 and node.getValid():
        print(prfix)
        wordSet.append(prfix)
    if prfix == '':
        options = letterGraph.get_vertices()
    else:
        options = letterGraph.get_neighbors(prfix[-1])
    for element in options:
        if element in node.children:
            traverse(node.children[element], prfix+element, letterGraph)

def solutions(word_list, chars, nytSol):
    output = []
    print(len(nytSol))
    print(nytSol)
    if len(nytSol)> 0:
        print("im inside")
        output.append([nytSol[0].lower(),nytSol[1].lower()])
    for word in word_list:
        last = word[len(word)-1]
        matches = [w for w in word_list if w[0] == last and w!= word]
        for m in matches:
            pair = word + m
            if set(pair) == chars:
                output.append([word,m])
    print(len(output))
    return output

def getSolutions(letters, trie, nytSol):
    print(letters)
    print(nytSol)
    global wordSet
    wordSet = []
    g = GetDictionary.createletterGraph(letters)
    letterSet = GetDictionary.createLetterSet(letters)
    traverse(trie.getRoot(), '', g)
    return solutions(wordSet, letterSet, nytSol)