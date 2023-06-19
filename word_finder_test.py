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