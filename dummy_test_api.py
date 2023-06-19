import requests


print(requests.get(
    "http://127.0.0.1:80/",
).json())

print(requests.post(
    "http://127.0.0.1:80/",
    json={"board": {2: "C"}, "letters": "at"}
).json())
