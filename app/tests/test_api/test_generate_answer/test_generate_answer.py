import json
from unittest.mock import patch, MagicMock

import pytest

from main import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@patch("api.generate_answer.generate_answer.PIIMask")
@patch("api.generate_answer.generate_answer.client")
def test_generate_answer(mock_inference_client, mock_pii_mask, client):

    # Mock the Pii class
    mock_pii_instance = mock_pii_mask.return_value
    mock_pii_instance.mask.return_value = {"context": "masked context", "prompt": "masked prompt"}
    mock_pii_instance.unmask.return_value = "unmasked response"

    # Mock the InferenceClient
    mock_stream = MagicMock()
    mock_stream.choices = [MagicMock(message=MagicMock(content="fake content"))]
    mock_inference_client.return_value.chat.completions.create.return_value = mock_stream

    # Mock request data
    data = {"context": "Call me at 555-123-4567.", "prompt": "Who am I?"}
    response = client.post("/generate-answer/", data=json.dumps(data), content_type="application/json")

    # Validate response
    assert response.status_code == 200
    assert response.json == {"response": "unmasked response"}
