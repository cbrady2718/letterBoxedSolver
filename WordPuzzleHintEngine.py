class WordPuzzleHintEngine:
    def __init__(self, solutions):
        self.solutions = solutions  # List of word pairs that are valid solutions
        self.word_patterns = self._build_word_patterns()

    def anchors(self):
        firsts = set()
        seconds = set()
        useful = []
        for element in self.solutions:
            firsts.add(element[0])
            seconds.add(element[1])
        for element in seconds:
            useful.append(element[0])
        return useful

    def _build_word_patterns(self):
        # Create patterns from solutions for faster matching
        patterns = {}
        for first_word, second_word in self.solutions:
            # Store word lists by their prefixes for faster lookups
            for word in [first_word, second_word]:
                for i in range(1, len(word) + 1):
                    prefix = word[:i]
                    if prefix not in patterns:
                        patterns[prefix] = []
                    patterns[prefix].append(word)
        return patterns
    
    def get_hint(self, progress):
        """
        Generate hints based on current progress
        
        progress: Can be:
            - [complete_word, partial_word_prefix]
            - [partial_word_prefix, complete_word]
            - [partial_word_prefix]
            - [complete_word]
        """
        for i in range(len(progress)):
            progress[i] = progress[i].lower()
        print(progress)
        if len(progress) == 2:
            # Case: One complete word and one partial word
            if self._is_complete_solution(progress[0]) and not self._is_complete_solution(progress[1]):
                return self._hint_for_complete_and_partial(progress[0], progress[1])
            elif self._is_complete_solution(progress[1]) and not self._is_complete_solution(progress[0]):
                return self._hint_for_complete_and_partial(progress[1], progress[0])
            else:
                return self.get_hint(progress[0])
        elif len(progress) == 1:
            # Case: Just one partial word
            if not self._is_in_solutions(progress[0]):
                return self._hint_for_partial(progress[0])
            # Case: Just one complete word
            else:
                return self._hint_for_complete(progress[0])
                
        return "I don't have enough information to provide a hint."
    
    def _is_complete_solution(self, word):
        # Check if a word is a complete solution word
        for element in self.solutions:
            if word == element[0] or word == element[1]:
                return True
        return False
    
    def _is_in_solutions(self, word):
        # Check if a word appears in solutions (either as complete or partial)
        for first, second in self.solutions:
            if word == first or word == second:
                return True
            if first.startswith(word) or second.startswith(word):
                return False  # It's a partial match
        return False
    
    def _hint_for_complete_and_partial(self, complete_word, partial_word):
        # Find potential matches where complete_word is part of a solution
        potential_pairs = []
        for first, second in self.solutions:
            if first == complete_word:
                potential_pairs.append(second)
            elif second == complete_word:
                potential_pairs.append(first)
        
        if not potential_pairs:
            return f"'{complete_word}' doesn't seem to be part of any solution."
        
        # Find candidates that match the partial pattern (prefix)
        candidates = []
        for word in potential_pairs:
            if word.startswith(partial_word):
                candidates.append(word)
        
        if not candidates:
            return f"The word '{partial_word}' doesn't match with '{complete_word}'."
        
        # Generate appropriate hint
        if len(candidates) == 1:
            target = candidates[0]
            if len(partial_word) < len(target):
                next_letter = target[len(partial_word)]
                return f"Try adding the letter '{next_letter}' next."
            else:
                return f"You've completed the word '{target}' that pairs with '{complete_word}'."
        else:
            # Check if all candidates have the same next letter
            if all(c[len(partial_word)] == candidates[0][len(partial_word)] for c in candidates if len(c) > len(partial_word)):
                next_letter = candidates[0][len(partial_word)]
                return f"The next letter is '{next_letter}'."
            else:
                possible_next = [c[len(partial_word)] for c in candidates if len(c) > len(partial_word)]
                return f"Possible next letters: {', '.join(set(possible_next))}"
    
    def _hint_for_partial(self, partial_word):
        # Find all potential completions for this prefix
        candidates = []
        for first, second in self.solutions:
            if first.startswith(partial_word):
                candidates.append(first)
            if second.startswith(partial_word):
                candidates.append(second)
        
        if not candidates:
            return "I don't recognize any words starting with this prefix."
        
        # Generate hint about the next letter
        if len(candidates) == 1:
            target = candidates[0]
            if len(partial_word) < len(target):
                next_letter = target[len(partial_word)]
                return f"The next letter is '{next_letter}'."
            else:
                return f"You've completed the word '{target}'."
        else:
            # Check if all candidates have the same next letter
            if all(c[len(partial_word)] == candidates[0][len(partial_word)] for c in candidates if len(c) > len(partial_word)):
                next_letter = candidates[0][len(partial_word)]
                return f"The next letter is '{next_letter}'."
            else:
                possible_next = [c[len(partial_word)] for c in candidates if len(c) > len(partial_word)]
                possible_next = list(set(possible_next))  # Remove duplicates
                
                # Filter by available letters
                available_next = [l for l in possible_next]
                
                if available_next:
                    if len(available_next) == 1:
                        return f"Try the letter '{available_next[0]}' next."
                    else:
                        return f"Consider one of these letters next: {', '.join(available_next)}"
                else:
                    return f"There are {len(candidates)} possible words that start with '{partial_word}'."
    
    def _hint_for_complete(self, complete_word):
        # Find potential paired words
        paired_candidates = []
        
        for first, second in self.solutions:
            if first == complete_word:
                paired_candidates.append(second)
            elif second == complete_word:
                paired_candidates.append(first)
        
        if not paired_candidates:
            return f"'{complete_word}' doesn't match any of my known solutions."
        
        # Generate hint about the paired word
        if len(paired_candidates) == 1:
            paired_word = paired_candidates[0]
            first_letter = paired_word[0]
            return f"Look for a {len(paired_word)}-letter word that starts with '{first_letter}' and pairs with '{complete_word}'."
        else:
            lengths = set(len(word) for word in paired_candidates)
            starting_letters = set(word[0] for word in paired_candidates)
            
            if len(starting_letters) == 1:
                return f"The paired word starts with '{list(starting_letters)[0]}'."
            elif len(lengths) == 1:
                return f"The paired word should be {list(lengths)[0]} letters long."
            else:
                return f"There are multiple possible pairs for '{complete_word}'."

