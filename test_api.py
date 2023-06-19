import requests

print(requests.post(
    "http://127.0.0.1:8000/",
    json={"board": {2: "C"}, "letters": "at"}
).json())
