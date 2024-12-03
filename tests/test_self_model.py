import uuid
import pytest
import epistemic_me

@pytest.fixture
def client():
    return epistemic_me.create("test_api_key")

def test_create_self_model(client):
    self_model_id = str(uuid.uuid4())
    self_obj = epistemic_me.SelfModel.create(id=self_model_id)
    assert "id" in self_obj
    assert "philosophies" in self_obj
    assert "belief_system" in self_obj
    assert "observation_contexts" in self_obj

def test_get_self(client):
    self_obj = epistemic_me.SelfModel.get_self("self_001")
    assert "id" in self_obj
    assert "philosophies" in self_obj
    assert "belief_system" in self_obj
    assert "observation_contexts" in self_obj

def test_add_philosophy(client):
    updated_self = epistemic_me.Philosophy.create("phil_105", self_model_id="self_001")
    assert "phil_105" in updated_self["philosophies"]
