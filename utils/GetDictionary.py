import json
from bs4 import BeautifulSoup
import requests
import re
import utils.trieClass as trieClass
from utils.UndirectedGraph import UndirectedGraph


def getDict(isNYT):
    outDict = {}
    if isNYT:
        dataDict = getNYTData()
        trie = trieClass.Trie()
        theirSol = dataDict['ourSolution']
        for element in dataDict['dictionary']:
            trie.insert(element.lower())
        outDict["trie"] = trie
        outDict["solution"] = theirSol
        outDict["isNYT"] = True
    else:
        outDict["trie"] = trieClass.load_trie_mmap("betterwords.pickle")
        outDict["isNYT"] = False
        outDict["solution"] = ""
    return outDict

def getNYTData():
    #key returns: ourSolution, dictionary, isNYT
    urlpage = 'https://www.nytimes.com/puzzles/letter-boxed'
    page = requests.get(urlpage)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page.content, 'html.parser')
    script_tag = soup.find('script', type='text/javascript', string=re.compile('window.gameData'))
    pattern = r'window\.gameData\s*=\s*({[^;]*})'
    contents = re.search(pattern, script_tag.string)
    contents = contents.group(1)
    full_data = json.loads(contents)
    full_data["isNYT"] = True
    return full_data


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