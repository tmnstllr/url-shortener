import validators
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
    urls[target_url] = generate(size=8)
    return f"{target_url}: {urls[target_url]}"
