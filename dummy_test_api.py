import requests


print(requests.get(
    "http://127.0.0.1:8000/",
).json())

print(requests.post(
    "http://127.0.0.1:8000/",
    json={"board": {0: "", 1: "", 2: "C"}, "letters": "at"}
).json())
