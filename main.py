import validators
import json
from fastapi import FastAPI, HTTPException
from nanoid import generate

app = FastAPI()

urls = {}


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.post("/encode")
def encode_url(target_url: str):
    if not validators.url(target_url):
        raise_bad_request(message="Provided URL is not valid")
    id = generate(size=8)
    clicks = 0
    urls[id] = {
        "target_url": target_url,
        "clicks": clicks
    }
    return {
        "id": id,
        "target_url": target_url,
        "clicks": clicks
    }


@app.post("/decode/{id}")
def decode_url(id: str):
    if id not in urls.keys():
        raise_bad_request(message="Shortened url id not found")
    return {
        "id": id,
        "target_url": urls[id]["target_url"],
        "clicks": urls[id]["clicks"]
    }
