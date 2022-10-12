import validators
import json
from fastapi import FastAPI, HTTPException
from nanoid import generate

app = FastAPI()

urls = {}


class Url:
    def __init__(self, target_url: str, clicks: int):
        self.target_url = target_url
        self.clicks = clicks


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


@app.post("/encode")
def encode_url(target_url: str):
    if not validators.url(target_url):
        raise_bad_request(message="Provided URL is not valid")
    id = generate(size=8)
    url = Url(target_url, 0)
    urls[id] = [{
        "target_url": url.target_url,
        "clicks": url.clicks
    }]
    return json.dumps({
        "id": id,
        "target_url": url.target_url,
        "clicks": url.clicks
    })