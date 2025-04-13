def validateWord(word):
    if len(word) < 3:
        print(word)
        print("length is invalid")
        return False
    if not word.isalpha():
        print(word)
        print("non letter characters")
        return False
    for i in range(1,len(word)):
        if word[i] == word[i-1]:
            print(word)
            print('repeat letters')
            return False
    return True


with open("wordlist") as inFile:
    lines = [line.rstrip('\n') for line in inFile]
    inFile.close()

with open("new_word_list.txt", "w") as f:
    for element in lines:
        if validateWord(element):
            f.write(element+'\n')
        else:
            print('invalid')
