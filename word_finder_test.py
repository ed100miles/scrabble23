import unittest
from scrabble23 import WordFinder


class TestWordFinder(unittest.TestCase):
    def setUp(self) -> None:
        self.test_board = ["" for _ in range(225)]

    def test_chunk_find_catches_bottom_right(self):
        self.test_board[-1] = "D"
        assert 'GOOD' in WordFinder('GOO', self.test_board).chunk_find()

    def test_chunk_find_with_board_rotation(self):
        self.test_board[14] = "C"
        assert 'CAT' in WordFinder('AT', self.test_board).chunk_find()

    def test_chunk_find_only_if_using_board_letters(self):
        self.test_board[0] = "C"
        assert 'AT' not in WordFinder('at', self.test_board).chunk_find()

    def test_find_words_with_empty_board(self):
        print(WordFinder('CAT', self.test_board).find_words())
        assert list(WordFinder('CAT', self.test_board).find_words().keys()) == [
            "CAT", "ACT", "AT", "TA"]

    def test_find_words_with_not_empty_board(self):
        self.test_board[0] = "C"
        assert "CAT" in WordFinder('AT', self.test_board).find_words()

    def test_find_words_not_existing_words(self):
        for key, val in {94: 'O', 95: 'C', 96: 'T', 97: 'O', 98: 'P', 99: 'U', 100: 'S'}.items():
            self.test_board[key] = val
        found_words = WordFinder('AT', self.test_board).find_words()
        assert "OCTOPUS" not in found_words

    def test_find_words_append_existing(self):
        for key, val in {94: 'F', 95: 'O', 96: 'X'}.items():
            self.test_board[key] = val
        found_words = WordFinder('ES', self.test_board).find_words()
        assert "FOXES" in found_words

    def test_find_words_no_nonsensiffying_letters_before(self):
        for key, val in {94: 'D', 95: 'O', 96: 'N', 97: 'E'}.items():
            self.test_board[key] = val
        found_words = WordFinder('EDING', self.test_board).find_words()
        assert "NEEDING" not in found_words

    def test_find_words_no_nonsensiffying_letters_after(self):
        for key, val in {93: 'A', 94: 'R', 95: 'T', 96: 'I', 97: 'S', 98: 'T', 99: 'S'}.items():
            self.test_board[key] = val
        found_words = WordFinder('F', self.test_board).find_words()
        assert "FART" not in found_words

    # TODO:
    # def test_find_words_no_nonsensiffying_letters_adjacent(self):
    #     for key, val in {93: 'A', 94: 'R', 95: 'T', 96: 'I', 97: 'S', 98: 'T', 99: 'S',
    #                      113: 'I', 128: 'P', 143: 'S', 144: 'O'}.items():
    #         self.test_board[key] = val
    #     found_words = WordFinder('MITH', self.test_board).find_words()
    #     assert "SMITH" not in found_words

    def test_find_words_no_nested_words(self):
        for key, val in {94: 'C', 95: 'H', 96: 'E', 97: 'E', 98: 'S', 99: 'E', 100: 'S'}.items():
            self.test_board[key] = val
        found_words = WordFinder('AT', self.test_board).find_words()
        assert "CHEESE" not in found_words
