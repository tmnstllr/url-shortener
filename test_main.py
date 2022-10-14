import json
from urllib.parse import quote
from fastapi.testclient import TestClient
from main import app
from helpers import detail_bad_request, detail_not_found

client = TestClient(app)

valid_url = "https://ms.com"
invalid_url = "google.de"
invalid_id = "b7fYtzC9"


def encode_url(url: str):
    return quote(url)


def test_encode_url():
    response = client.post(f"/encode?target_url={encode_url(valid_url)}")
    assert response.status_code == 200
    assert len(response.json()["id"]) == 8
    assert response.json()["target_url"] == valid_url
    assert response.json()["clicks"] == 0


def test_encode_url_bad_request():
    response = client.post(f"/encode?target_url={encode_url(invalid_url)}")
    assert response.status_code == 400
    assert response.json()["detail"] == detail_bad_request


def test_decode_url_id_not_found():
    response = client.get(f"/decode/{invalid_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == detail_not_found


def test_encode_decode_url():
    encode_response = client.post(f"/encode?target_url={encode_url(valid_url)}")
    id = encode_response.json()["id"]
    decode_response = client.get(f"/decode/{id}")
    assert decode_response.status_code == 200
    assert len(decode_response.json()["id"]) == 8
    assert decode_response.json()["target_url"] == valid_url
    assert decode_response.json()["clicks"] == 0


def test_redirect_url_id_not_found():
    response = client.get(f"/r/{invalid_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == detail_not_found


def test_encode_redirect_decode_url():
    encode_response = client.post(f"/encode?target_url={encode_url(valid_url)}")
    id = encode_response.json()["id"]
    redirect_response = client.get(f"/r/{id}")
    assert redirect_response.status_code == 404
    decode_response = client.get(f"/decode/{id}")
    assert decode_response.status_code == 200
    assert len(decode_response.json()["id"]) == 8
    assert decode_response.json()["target_url"] == valid_url
    assert decode_response.json()["clicks"] == 1
