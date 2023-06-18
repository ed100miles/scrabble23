import numpy as np
import json
from collections import Counter
from typing import Dict

LettersCounter = Dict[str, int]
TrieNode = Dict[str, str]


trie_path = "trie.json"


class WordFinder():
    """Class encapsulating trie data structure, users letters and the method
    to find playable words"""

    def __init__(self, user_letters: str, board_array: list[str]) -> None:
        with open(trie_path) as trie_file:
            self.trie: Dict = json.load(trie_file)
        self.found_words: Dict[str, str] = {}
        self.user_letters_counter: LettersCounter = Counter(
            user_letters.upper())
        self.board_array = np.array(board_array).reshape(15, 15)

    def find_words(self, node, node_depth, chunk, letters_counter=None):
        if letters_counter is None:
            letters_counter = self.user_letters_counter.copy()
        letters_counter_copy = letters_counter.copy()
        if 'word' in node:
            self.found_words[node['word']] = node['definition']
        if node_depth == len(node):
            return
        if chunk[node_depth] != "" and chunk[node_depth] in letters_counter:
            if letters_counter[chunk[node_depth]] > 0:
                letters_counter_copy[chunk[node_depth]
                                     ] = letters_counter[chunk[node_depth]]-1
                self.find_words(node[chunk[node_depth]],
                                node_depth+1, chunk, letters_counter_copy)
            return
        for letter in letters_counter:
            if letters_counter[letter] > 0:
                letters_counter_copy[letter] = letters_counter_copy[letter] - 1
                if letters_counter_copy[letter] <= 0:
                    del letters_counter_copy[letter]
                self.find_words(node[letter], node_depth+1,
                                chunk, letters_counter_copy)

    def chunk_find(self):
        for chunk_length in range(2, len(self.board_array[0])+1):
            for chunk_start_position in range(16-chunk_length):
                for row in self.board_array:
                    chunk = row[chunk_start_position:chunk_length +
                                chunk_start_position]
                    print(
                        f'len: {chunk_length}, start: {chunk_start_position}')
                    self.find_words(self.trie, 0, chunk, self.user_letters_counter)

    # def find_words(self):
        # for index, row in enumerate(self.board_array):
        #     for chunk_length in range(2, len(row)):
                # for chunk_position in range(len(row)-chunk_length):
                #     print(row[chunk_position:chunk_length+1])
                    # print(f"{chunk_position} + {chunk_length} = {chunk_length+chunk_position}")

    # def find_words(
    #     self,
    #     user_letters_counter: Dict[str, int] | None = None,
    #     node: Union[Dict, None] = None
    # ) -> Dict[str, str]:
    #     """Recursive method for trie search, adds word to self.found_words
    #     dict if 'word' key is in the current trie node"""
    #     print(self.board_array)
    #     if user_letters_counter is None:
    #         user_letters_counter = self.base_user_letters_counter
    #     if node is None:
    #         node = self.trie
    #     if 'word' in node:
    #         self.found_words[node['word']] = node['definition']
    #     for letter, count in user_letters_counter.items():
    #         if count > 0 and letter in node:
    #             counter_copy = user_letters_counter.copy()
    #             counter_copy[letter] = counter_copy[letter] - 1
    #             self.find_words(counter_copy, node[letter])
    #     return self.found_words


test_board = ["" for _ in range(225)]
test_board[-1] = "Z"
WordFinder('aetursn', test_board).chunk_find()
