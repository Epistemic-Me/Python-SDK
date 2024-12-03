import pytest
from epistemic_me import create

@pytest.fixture
def client():
    return create("test_api_key")

def test_create_philosophy(client):
    philosophy = client.philosophy.create("Test philosophy text", extrapolate_contexts=False)
    assert "id" in philosophy

def test_add_observation_contexts(client):
    updated_philosophy = client.philosophy.add_observation_contexts(
        "phil_001",
        new_observation_contexts={
            "context1": {
                "description": "Test context",
                "evidencable_details": {
                    "inputs": [{"type": "FLOAT", "units": "hours per night", "name": "sleep"}],
                    "outputs": [{"type": "INT", "units": "milliseconds", "name": "hrv"}]
                }
            }
        }
    )
    assert "context1" in updated_philosophy["observation_contexts"]
