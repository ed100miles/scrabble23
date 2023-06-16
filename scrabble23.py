import json
from collections import Counter
from typing import Dict, Union

LettersCounter = Dict[str, int]
TrieNode = Dict[str, str]

trie_path = "trie.json"


class WordFinder():
    """Class encapsulating trie data structure, users letters and the method
    to find playable words"""

    def __init__(self, user_letters: str) -> None:
        with open(trie_path) as trie_file:
            self.trie: Dict = json.load(trie_file)
        self.found_words: Dict[str, str] = {}
        self.base_user_letters_counter: LettersCounter = Counter(
            user_letters.upper())

    def find_words(
        self,
        user_letters_counter: Dict[str, int] | None = None,
        node: Union[Dict, None] = None
    ) -> Dict[str, str]:
        """Recursive method for trie search, adds word to self.found_words
        dict if 'word' key is in the current trie node"""
        if user_letters_counter is None:
            user_letters_counter = self.base_user_letters_counter
        if node is None:
            node = self.trie
        if 'word' in node:
            self.found_words[node['word']] = node['definition']
        for letter, count in user_letters_counter.items():
            if count > 0 and letter in node:
                counter_copy = user_letters_counter.copy()
                counter_copy[letter] = counter_copy[letter] - 1
                self.find_words(counter_copy, node[letter])
        return self.found_words


WordFinder('aet;onva;orinac;ornauernaciursn').find_words()
