import pytest
import uuid
import epistemic_me

@pytest.fixture(autouse=True)
def setup_epistemic_me():
    epistemic_me.create("test_api_key", "localhost:8080")

def test_self_model_integration():
    # Test CreateSelfModel
    user_id = str(uuid.uuid4())
    create_self_model_response = epistemic_me.SelfModel.create(id=user_id)
    assert create_self_model_response['selfModel']['id'] == user_id
    assert create_self_model_response['selfModel']['philosophies'] == ["default"]

    # Test RetrieveSelfModel
    get_self_model_response = epistemic_me.SelfModel.retrieve(self_id=user_id)
    assert get_self_model_response['selfModel']['id'] == user_id
    assert get_self_model_response['selfModel']['philosophies'] == ["default"]

    # Test ListDialectics
    list_dialectics_response = epistemic_me.SelfModel.list_dialectics(self_model_id=user_id)
    assert isinstance(list_dialectics_response, dict)
    assert isinstance(list_dialectics_response.get('dialectics', []), list)

def test_create_self_model():
    user_id = str(uuid.uuid4())
    response = epistemic_me.SelfModel.create(id=user_id)
    assert response['selfModel']['id'] == user_id
    assert response['selfModel']['philosophies'] == ["default"]

def test_retrieve_self_model():
    user_id = str(uuid.uuid4())
    epistemic_me.SelfModel.create(id=user_id)
    response = epistemic_me.SelfModel.retrieve(self_id=user_id)
    assert response['selfModel']['id'] == user_id
    assert response['selfModel']['philosophies'] == ["default"]

def test_retrieve_belief_system():
    user_id = str(uuid.uuid4())
    epistemic_me.SelfModel.create(id=user_id)
    response = epistemic_me.SelfModel.retrieve_belief_system(self_model_id=user_id)
    assert 'beliefSystem' in response
    assert 'beliefs' in response['beliefSystem']
    assert 'observationContexts' in response['beliefSystem']

def test_list_dialectics():
    user_id = str(uuid.uuid4())
    epistemic_me.SelfModel.create(id=user_id)
    response = epistemic_me.SelfModel.list_dialectics(self_model_id=user_id)
    assert isinstance(response, dict)
    assert isinstance(response.get('dialectics', []), list)
