from fastapi import FastAPI
from typing import Dict, TypedDict
from scrabble23 import WordFinder

app = FastAPI()


class PostData(TypedDict):
    board: Dict[int, str]
    letters: str


@app.post("/")
async def read_root(data: PostData):
    board = ["" for _ in range(225)]
    for index, value in data['board'].items():
        board[index] = value
    words = WordFinder(data['letters'], board).find_words()
    return {'foundWords': words}

# uvicorn api:app --reload
