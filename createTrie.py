"""
Script to convert {word:definition} JSON into trie data structure for
efficient searching. See https://en.wikipedia.org/wiki/Trie
"""

import json
from typing import Tuple, Dict, Any


WordList = list[Tuple[str, str]]
TrieNode = Dict[str, Any]

trie: TrieNode = {}

with open('scrabbleWords.json') as words_file:
    word_list: WordList = list(json.load(words_file).items())

for word, definition in word_list:
    node: TrieNode = trie
    for index, letter in enumerate(word):
        is_word = index+1 == len(word)
        if letter not in node:
            node[letter] = {}
        if is_word:
            node[letter]['word'] = word
            node[letter]['definition'] = definition
        node = node[letter]

with open('trie.json', 'w') as trie_file:
    json.dump(trie, trie_file)
