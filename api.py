from fastapi import FastAPI
from typing import Dict, TypedDict
from scrabble23 import WordFinder
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PostData(TypedDict):
    board: Dict[int, str]
    letters: str


@app.get("/")
def test():
    return {"listening"}


@app.post("/")
async def read_root(data: PostData):
    if True:
        clean_board = {k: v for k, v in data['board'].items() if v != ""}
        print(clean_board)
    board = ["" for _ in range(225)]
    for index, value in data['board'].items():
        board[index] = value
    words = WordFinder(data['letters'], board).find_words()
    return {'found': words}

# uvicorn api:app --reload
