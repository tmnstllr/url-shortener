import json
from urllib.parse import quote
from fastapi.testclient import TestClient
from .main import app
from .helpers import detail_bad_request, detail_not_found

client = TestClient(app)


def encode_url(url: str):
    return quote(url)


def test_encode_url():
    url = "https://ms.com"
    response = client.post(f"/encode?target_url={encode_url(url)}")
    assert response.status_code == 200
    assert len(response.json()["id"]) == 8
    assert response.json()["target_url"] == "https://ms.com"
    assert response.json()["clicks"] == 0


def test_encode_url_bad_request():
    url = "google.de"
    response = client.post(f"/encode?target_url={encode_url(url)}")
    assert response.status_code == 400
    assert response.json()["detail"] == detail_bad_request


def test_decode_url_id_not_found():
    id = "ASDASD45"
    response = client.get(f"/decode/{id}")
    assert response.status_code == 404
    assert response.json()["detail"] == detail_not_found
