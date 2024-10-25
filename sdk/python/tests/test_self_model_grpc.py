import pytest
import uuid
import epistemic_me

@pytest.fixture
def client():
    return epistemic_me.create("", "localhost:8080")

@pytest.fixture
def authenticated_client(client):
    # Create a developer
    developer_name = f"Test Developer {uuid.uuid4()}"
    developer_email = f"test_{uuid.uuid4()}@example.com"
    developer = epistemic_me.Developer.create(name=developer_name, email=developer_email)
    
    # Fetch the developer to get the API key
    developer_with_key = epistemic_me.Developer.retrieve(developer_id=developer["id"])
    
    # Return both the authenticated client and the developer info
    return {
        "client": epistemic_me.create(developer_with_key["apiKeys"][0], "localhost:8080"),
        "developer": developer_with_key
    }

def test_self_model_integration(authenticated_client):
    # Test CreateSelfModel
    self_model_id = str(uuid.uuid4())
    create_self_model_response = epistemic_me.SelfModel.create(id=self_model_id)
    assert create_self_model_response['selfModel']['id'] == self_model_id
    assert create_self_model_response['selfModel']['philosophies'] == ["default"]

    # Test RetrieveSelfModel
    get_self_model_response = epistemic_me.SelfModel.retrieve(self_id=self_model_id)
    assert get_self_model_response['selfModel']['id'] == self_model_id
    assert get_self_model_response['selfModel']['philosophies'] == ["default"]

    # Test ListDialectics
    list_dialectics_response = epistemic_me.SelfModel.list_dialectics(self_model_id=self_model_id)
    assert isinstance(list_dialectics_response, dict)
    assert isinstance(list_dialectics_response.get('dialectics', []), list)

def test_create_self_model(authenticated_client):
    self_model_id = str(uuid.uuid4())
    response = epistemic_me.SelfModel.create(id=self_model_id)
    assert response['selfModel']['id'] == self_model_id
    assert response['selfModel']['philosophies'] == ["default"]

def test_retrieve_self_model(authenticated_client):
    self_model_id = str(uuid.uuid4())
    epistemic_me.SelfModel.create(id=self_model_id)
    response = epistemic_me.SelfModel.retrieve(self_id=self_model_id)
    assert response['selfModel']['id'] == self_model_id
    assert response['selfModel']['philosophies'] == ["default"]

# def test_retrieve_belief_system():
#     self_model_id = str(uuid.uuid4())
#     response_create = epistemic_me.SelfModel.create(id=self_model_id)
#     print(response_create)
#     response = epistemic_me.SelfModel.retrieve_belief_system(self_model_id=self_model_id)
#     print(response)
#     assert 'beliefSystem' in response
#     assert 'beliefs' in response['beliefSystem']
#     assert 'observationContexts' in response['beliefSystem']

def test_list_dialectics(authenticated_client):
    self_model_id = str(uuid.uuid4())
    epistemic_me.SelfModel.create(id=self_model_id)
    response = epistemic_me.SelfModel.list_dialectics(self_model_id=self_model_id)
    assert isinstance(response, dict)
    assert isinstance(response.get('dialectics', []), list)
