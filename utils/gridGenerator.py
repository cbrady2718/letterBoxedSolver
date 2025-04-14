import random


def generateGrid(num_unique_letters=12):
    with open("oxford5000.txt") as inFile:
        lines = [line.rstrip('\n') for line in inFile]
        inFile.close()

    wordDict = {}
    for line in lines:
        if line[0] in wordDict:
            cur = wordDict[line[0]]
            cur.append(line)
            wordDict[line[0]] = cur
        else:
            wordDict[line[0]] = [line]
    

    def find_pairs_with_unique_letters(words, num_unique_letters=12):
        # List to store valid pairs
        valid_pairs = []
        
        # Iterate through all possible pairs
        for i in range(len(words)):
            word1 = words[i]
            for element in wordDict[word1[-1]]:
                newWord = word1 + element
                unique_letters = set(newWord)
                if len(unique_letters) == num_unique_letters:
                    valid_pairs.append((word1,element))
            
        return valid_pairs


    def fillOut(letters, prev_side, sides, max_side_length=3):
        # Base case: all letters placed successfully
        if not letters:
            return (True, sides)
        
        cur_letter = letters[0]
        rest_of_word = letters[1:]
        
        # Check if cur_letter is already in a side
        for i in range(4):
            if cur_letter in sides[i]:
                # If the letter is on the same side as the previous letter, invalid
                if i == prev_side:
                    return (False, sides)
                # Otherwise, try this side and recurse
                return fillOut(rest_of_word, i, sides, max_side_length)
        
        # If letter not found, try placing it in each valid side
        outputs = []
        for i in range(4):
            # Skip if side is full or same as previous side
            if len(sides[i]) >= max_side_length or i == prev_side:
                outputs.append((False, sides))
                continue
            # Create a deep copy of sides
            new_sides = [side[:] for side in sides]
            new_sides[i].append(cur_letter)
            # Recurse with updated sides and current side as prev_side
            result = fillOut(rest_of_word, i, new_sides, max_side_length)
            outputs.append(result)
        
        # Return the first valid result, or invalid if none
        for result in outputs:
            if result[0]:
                return result
        return (False, sides)

    # Helper function to initialize and call fillOut
    def create_letterboxed_grid(word1, word2, max_side_length=3):
        # Combine letters: word1 + word2[1:] (since word2 starts with word1's last letter)
        letters = word1 + word2[1:]
        # Initialize empty sides
        sides = [[], [], [], []]
        # Start with no previous side (-1)
        result, final_sides = fillOut(letters, -1, sides, max_side_length)
        if result:
            return final_sides
        return None
    def scramble_grid(sides):
        # Create a deep copy of the sides to avoid modifying the input
        scrambled_sides = [side[:] for side in sides]
        
        # Randomize letter order within each side
        for i in range(len(scrambled_sides)):
            random.shuffle(scrambled_sides[i])
        
        # Randomize the order of the sides
        random.shuffle(scrambled_sides)
        
        return scrambled_sides


    # Test the function
    pairs = find_pairs_with_unique_letters(lines, num_unique_letters)  # Default to 12 for 3x4 grid
    max_side_length = num_unique_letters // 4
    looking = True
    while looking:
        index = random.randint(0,len(pairs)-1)
        pair = pairs[index]
        grid = create_letterboxed_grid(pair[0], pair[1], max_side_length)  # Default to 3x4 grid
        print(pair)
        if grid:
            print("Valid grid:", grid)
            newGrid = scramble_grid(grid)
            print("Scrambled grid: ",newGrid)
            return newGrid, pair
        else:
            print("invalid")
                        

