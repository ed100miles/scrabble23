import numpy as np
import json
from collections import Counter
from typing import Dict, Any, List

LettersCounter = Dict[str, int]
TrieNode = Dict[str, Any]


trie_path = "trie.json"


class WordFinder():
    """Class encapsulating trie data structure, users letters and the method
    to find playable words"""

    def __init__(self, user_letters: str, board_array: list[str]) -> None:
        with open(trie_path) as trie_file:
            self.trie: Dict[str, Any] = json.load(trie_file)
        self.found_words: Dict[str, str] = {}
        self.user_letters_counter: LettersCounter = Counter(
            user_letters.upper())
        self.board_array = np.array(board_array).reshape(15, 15)

    def find_words(self):
        board_copy = self.board_array.copy()
        board_copy[board_copy == ""] = '0'
        board_copy[board_copy != "0"] = '1'
        if not np.array(board_copy, dtype=bool).any():  # if no letters on board
            return self._find_words()
        else:
            return self.chunk_find()

    def word_has_chunk_letters(self, word: List[str], chunk: List[str]):
        """Returns true if word has a letter thats at the same index as letters in the chunk"""
        return len(list(filter(lambda idx: idx[0] == idx[1], list(zip(word, chunk))))) > 0

    def find_words_in_chunk(self, node: TrieNode, node_depth: int, chunk: List[str],
                            letters_counter: LettersCounter):
        letters_counter_copy = letters_counter.copy()
        if 'word' in node and self.word_has_chunk_letters(node["word"], chunk):
            if node['word'] != ''.join(chunk) and node_depth == len(chunk):
                self.found_words[node['word']] = node['definition']
        if node_depth >= len(chunk):
            return
        # if there's a letter at this index of the chunk, we have to use it
        if chunk[node_depth] != '' and chunk[node_depth] in node:
            self.find_words_in_chunk(node[chunk[node_depth]],
                                     node_depth+1, chunk, letters_counter_copy)
        else:  # else we iterate through users remaining letters and recursively call find_words()
            for letter in letters_counter:
                # remove 0 count letters from counter to speed up (debateable)
                if letters_counter[letter] == 0:
                    del letters_counter_copy[letter]
                if letters_counter[letter] > 0 and letter in node:
                    letters_counter_copy[letter] -= 1
                    self.find_words_in_chunk(node[letter], node_depth+1,
                                             chunk, letters_counter_copy)

    def chunk_find(self):
        """Searches through the board in sliding chunks, looking for words"""
        for board_direction in range(2):
            if board_direction == 1:
                # 90 degree rotation gets words going down as well as across
                self.board_array = np.rot90(self.board_array)
            for chunk_length in range(2, len(self.board_array[0])+1):
                for chunk_start_position in range(16-chunk_length):
                    for row in self.board_array:
                        chunk = row[chunk_start_position:chunk_length +
                                    chunk_start_position]
                        if ''.join(chunk) != "":  # if chunk not empty
                            # and chunk not got any letters before or after it
                            # see test_find_words_no_nonsensiffying_letters_before/after()
                            if ((chunk_start_position == 0 or row[chunk_start_position-1] == "")
                                    and (chunk_start_position+len(chunk) == 15
                                         or row[chunk_start_position+len(chunk)] == "")):
                                self.find_words_in_chunk(self.trie, 0, chunk,
                                                         self.user_letters_counter)
        return self.found_words

    def _find_words(
        self,
        user_letters_counter: Any = None,
        node: Any = None
    ) -> Dict[str, str]:
        """Recursive method for trie search, adds word to self.found_words
        dict if 'word' key is in the current trie node, use this to search when
        there arent any letters on the board - it's exhastive"""
        if user_letters_counter is None:
            user_letters_counter = self.user_letters_counter
        if node is None:
            node = self.trie
        if 'word' in node:
            self.found_words[node['word']] = node['definition']
        for letter, count in user_letters_counter.items():
            if count > 0 and letter in node:
                counter_copy = user_letters_counter.copy()
                counter_copy[letter] = counter_copy[letter] - 1
                self._find_words(counter_copy, node[letter])
        return self.found_words
