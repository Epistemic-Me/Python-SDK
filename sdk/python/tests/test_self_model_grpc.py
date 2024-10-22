 
import pytest
import uuid
from epistemic_me.grpc_client import GrpcClient
from epistemic_me.generated.proto.models import dialectic_pb2

@pytest.fixture
def client():
    return GrpcClient('localhost:8080')

def test_self_model_integration(client):
    # Test CreateSelfModel
    user_id = str(uuid.uuid4())
    create_self_model_response = client.create_self_model(user_id, philosophies=["default"])
    assert create_self_model_response['selfModel']['id'] == user_id
    assert create_self_model_response['selfModel']['philosophies'] == ["default"]

    # Test GetSelfModel
    get_self_model_response = client.get_self_model(user_id)
    assert get_self_model_response['selfModel']['id'] == user_id
    assert get_self_model_response['selfModel']['philosophies'] == ["default"]

    # Test CreatePhilosophy
    create_philosophy_response = client.create_philosophy("Test philosophy", True)
    assert create_philosophy_response['philosophy']['description'] == "Test philosophy"
    assert create_philosophy_response['philosophy']['extrapolateContexts'] == True
    philosophy_id = create_philosophy_response['philosophy']['id']

    # Test AddPhilosophy
    add_philosophy_response = client.add_philosophy(user_id, philosophy_id)
    assert philosophy_id in add_philosophy_response['updatedSelfModel']['philosophies']

    # Test GetBeliefSystemOfSelfModel
    get_belief_system_response = client.get_self_model(user_id)
    assert 'beliefSystem' in get_belief_system_response['selfModel']
    assert len(get_belief_system_response['selfModel']['beliefSystem'].get('beliefs', [])) == 0
    assert len(get_belief_system_response['selfModel']['beliefSystem'].get('observationContexts', [])) == 0

    # Test ListDialecticsOfSelfModel
    create_dialectic_response = client.create_dialectic(user_id, dialectic_pb2.DialecticType.DEFAULT)
    assert 'dialecticId' in create_dialectic_response

    get_self_model_with_dialectics_response = client.get_self_model(user_id)
    assert len(get_self_model_with_dialectics_response['selfModel'].get('dialectics', [])) == 1
    assert get_self_model_with_dialectics_response['selfModel']['dialectics'][0]['id'] == create_dialectic_response['dialecticId']

def test_create_self_model(client):
    user_id = str(uuid.uuid4())
    response = client.create_self_model(user_id, philosophies=["default"])
    assert response['selfModel']['id'] == user_id
    assert response['selfModel']['philosophies'] == ["default"]

def test_get_self_model(client):
    user_id = str(uuid.uuid4())
    client.create_self_model(user_id, philosophies=["default"])
    response = client.get_self_model(user_id)
    assert response['selfModel']['id'] == user_id
    assert response['selfModel']['philosophies'] == ["default"]

def test_create_philosophy(client):
    response = client.create_philosophy("Test philosophy", True)
    assert response['philosophy']['description'] == "Test philosophy"
    assert response['philosophy']['extrapolateContexts'] == True

def test_add_philosophy(client):
    user_id = str(uuid.uuid4())
    client.create_self_model(user_id, philosophies=["default"])
    philosophy_response = client.create_philosophy("New philosophy", False)
    philosophy_id = philosophy_response['philosophy']['id']
    
    response = client.add_philosophy(user_id, philosophy_id)
    assert philosophy_id in response['updatedSelfModel']['philosophies']

def test_get_belief_system_of_self_model(client):
    user_id = str(uuid.uuid4())
    client.create_self_model(user_id, philosophies=["default"])
    response = client.get_self_model(user_id)
    assert 'beliefSystem' in response['selfModel']
    assert len(response['selfModel']['beliefSystem'].get('beliefs', [])) == 0
    assert len(response['selfModel']['beliefSystem'].get('observationContexts', [])) == 0

def test_list_dialectics_of_self_model(client):
    user_id = str(uuid.uuid4())
    client.create_self_model(user_id, philosophies=["default"])
    create_dialectic_response = client.create_dialectic(user_id, dialectic_pb2.DialecticType.DEFAULT)
    
    response = client.get_self_model(user_id)
    assert len(response['selfModel'].get('dialectics', [])) == 1
    assert response['selfModel']['dialectics'][0]['id'] == create_dialectic_response['dialecticId']
