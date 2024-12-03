import pytest
from epistemic_me import create

@pytest.fixture
def client():
    return create("test_api_key")

def test_create_dialectic(client):
    dialectic = client.dialectic.create("self_001")
    assert "id" in dialectic

def test_answer_dialectic(client):
    updated_dialectic = client.dialectic.answer("dialectic_001", "Test answer")
    assert "answer" in updated_dialectic
    assert updated_dialectic["answer"] == "Test answer"
