from fastapi import HTTPException
from nanoid import generate
import validators

detail_bad_request = "Provided URL is not valid"
detail_not_found = "Shortened url id not found"


def raise_bad_request():
    raise HTTPException(status_code=400, detail=detail_bad_request)


def raise_not_found():
    raise HTTPException(status_code=404, detail=detail_not_found)


def generate_id():
    return generate(size=8)


def is_valid_url(url: str):
    return validators.url(url)


def convert_to_json(url: str, clicks: int, id: str = None):
    if id is None:
        return {
            "target_url": url,
            "clicks": clicks
        }
    return {
        "id": id,
        "target_url": url,
        "clicks": clicks
    }
