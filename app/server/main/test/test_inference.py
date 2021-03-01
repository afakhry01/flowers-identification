import base64

from fastapi.testclient import TestClient
from main import app
from controller.inference import Inference

client = TestClient(app)

def test_true():
    with open("resources/test.jpg", "rb") as image:
        encoded = base64.b64encode(image.read())
    
    image = encoded.decode('utf8')
    response = client.post("/api/flowers/classify/", json={ "image": image})
    
    assert response.status_code == 200
    assert "classification" in response.json().keys()
    assert "confidence" in response.json().keys()
