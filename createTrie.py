"""
Script to convert {word:definition} JSON into trie data structure for
efficient searching. See https://en.wikipedia.org/wiki/Trie
"""

import json

with open('scrabbleWords.json') as words_file:
    word_list = list(json.load(words_file).items())

trie = {}

for word, definition in word_list:
    node = trie
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
