from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from helpers import raise_bad_request, raise_not_found, generate_id, is_valid_url, convert_to_json, id_exists

app = FastAPI()

urls = {}


@app.post("/encode")
def encode_url(target_url: str):
    if not is_valid_url(target_url):
        raise_bad_request()
    id = generate_id()
    clicks = 0
    urls[id] = convert_to_json(url=target_url, clicks=clicks)
    return convert_to_json(id=id, url=target_url, clicks=clicks)


@app.get("/decode/{id}")
def decode_url(id: str):
    if id_exists(urls, id):
        raise_not_found()
    return convert_to_json(id=id, url=urls[id]["target_url"], clicks=urls[id]["clicks"])


@app.get("/r/{id}")
def redirect_url(id: str):
    if id_exists(urls, id):
        raise_not_found()
    urls[id]["clicks"] += 1
    return RedirectResponse(urls[id]["target_url"])
