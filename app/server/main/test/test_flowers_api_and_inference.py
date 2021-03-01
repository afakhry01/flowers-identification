import base64
import copy
import pytest

from fastapi.testclient import TestClient
from main import app
from router.flowers import inferrer
from controller.inference import Inference

client = TestClient(app)

def test_classify_success():
    with open("resources/test.jpg", "rb") as image:
        encoded = base64.b64encode(image.read())
    
    image = encoded.decode('utf8')
    response = client.post("/api/flowers/classify/", json={ "image": image})
    
    assert response.status_code == 200
    assert "classification" in response.json().keys()
    assert "confidence" in response.json().keys()


def test_classify_failure():
    # Missing payload
    response = client.post("/api/flowers/classify/")
    assert response.status_code == 422

    # Sending wrong payload format
    response = client.post("/api/flowers/classify/", json={ "image": 0})
    assert response.status_code == 422
    assert response.json().get('detail') == 'Invalid Format'

    # Wrong namespace
    response = client.post("/api/flowers/classify", json={ "image": 0})
    assert response.status_code == 307

    response = client.post("/api/flowers/classify/123", json={ "image": 0})
    assert response.status_code == 404
    assert response.json().get('detail') == 'Not Found'

def test_exceptions():
    with open("resources/test.jpg", "rb") as image:
        f = image.read()

    # Test classes are not valid
    new_inferrer = copy.deepcopy(inferrer)
    new_inferrer.classes = None
    with pytest.raises(ValueError, match="Uninitialized classes"):
        new_inferrer.classify(f)

    # Test model is not valid
    new_inferrer.classes = inferrer.classes
    new_inferrer.model = None
    with pytest.raises(ValueError, match="Uninitialized model"):
        new_inferrer.classify(f)

    # Test model is not valid
    new_inferrer.model = inferrer.model
    new_inferrer.transforms = None
    with pytest.raises(ValueError, match="Uninitialized transforms"):
        new_inferrer.classify(f)
