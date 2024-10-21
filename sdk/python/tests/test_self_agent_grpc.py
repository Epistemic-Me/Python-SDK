import pytest
import uuid
from epistemic_me.grpc_client import GrpcClient
from epistemic_me.generated.proto.models import dialectic_pb2

@pytest.fixture
def client():
    return GrpcClient('localhost:8080')

def test_self_agent_integration(client):
    # Test CreateSelfAgent
    user_id = str(uuid.uuid4())
    create_self_agent_response = client.create_self_agent(user_id, philosophies=["default"])
    assert create_self_agent_response['selfAgent']['id'] == user_id
    assert create_self_agent_response['selfAgent']['philosophies'] == ["default"]

    # Test GetSelfAgent
    get_self_agent_response = client.get_self_agent(user_id)
    assert get_self_agent_response['selfAgent']['id'] == user_id
    assert get_self_agent_response['selfAgent']['philosophies'] == ["default"]

    # Test CreatePhilosophy
    create_philosophy_response = client.create_philosophy("Test philosophy", True)
    assert create_philosophy_response['philosophy']['description'] == "Test philosophy"
    assert create_philosophy_response['philosophy']['extrapolateContexts'] == True
    philosophy_id = create_philosophy_response['philosophy']['id']

    # Test AddPhilosophy
    add_philosophy_response = client.add_philosophy(user_id, philosophy_id)
    assert philosophy_id in add_philosophy_response['updatedSelfAgent']['philosophies']

    # Test GetBeliefSystemOfSelfAgent
    get_belief_system_response = client.get_self_agent(user_id)
    assert 'beliefSystem' in get_belief_system_response['selfAgent']
    assert len(get_belief_system_response['selfAgent']['beliefSystem'].get('beliefs', [])) == 0
    assert len(get_belief_system_response['selfAgent']['beliefSystem'].get('observationContexts', [])) == 0

    # Test ListDialecticsOfSelfAgent
    create_dialectic_response = client.create_dialectic(user_id, dialectic_pb2.DialecticType.DEFAULT)
    assert 'dialecticId' in create_dialectic_response

    get_self_agent_with_dialectics_response = client.get_self_agent(user_id)
    assert len(get_self_agent_with_dialectics_response['selfAgent'].get('dialectics', [])) == 1
    assert get_self_agent_with_dialectics_response['selfAgent']['dialectics'][0]['id'] == create_dialectic_response['dialecticId']

def test_create_self_agent(client):
    user_id = str(uuid.uuid4())
    response = client.create_self_agent(user_id, philosophies=["default"])
    assert response['selfAgent']['id'] == user_id
    assert response['selfAgent']['philosophies'] == ["default"]

def test_get_self_agent(client):
    user_id = str(uuid.uuid4())
    client.create_self_agent(user_id, philosophies=["default"])
    response = client.get_self_agent(user_id)
    assert response['selfAgent']['id'] == user_id
    assert response['selfAgent']['philosophies'] == ["default"]

def test_create_philosophy(client):
    response = client.create_philosophy("Test philosophy", True)
    assert response['philosophy']['description'] == "Test philosophy"
    assert response['philosophy']['extrapolateContexts'] == True

def test_add_philosophy(client):
    user_id = str(uuid.uuid4())
    client.create_self_agent(user_id, philosophies=["default"])
    philosophy_response = client.create_philosophy("New philosophy", False)
    philosophy_id = philosophy_response['philosophy']['id']
    
    response = client.add_philosophy(user_id, philosophy_id)
    assert philosophy_id in response['updatedSelfAgent']['philosophies']

def test_get_belief_system_of_self_agent(client):
    user_id = str(uuid.uuid4())
    client.create_self_agent(user_id, philosophies=["default"])
    response = client.get_self_agent(user_id)
    assert 'beliefSystem' in response['selfAgent']
    assert len(response['selfAgent']['beliefSystem'].get('beliefs', [])) == 0
    assert len(response['selfAgent']['beliefSystem'].get('observationContexts', [])) == 0

def test_list_dialectics_of_self_agent(client):
    user_id = str(uuid.uuid4())
    client.create_self_agent(user_id, philosophies=["default"])
    create_dialectic_response = client.create_dialectic(user_id, dialectic_pb2.DialecticType.DEFAULT)
    
    response = client.get_self_agent(user_id)
    assert len(response['selfAgent'].get('dialectics', [])) == 1
    assert response['selfAgent']['dialectics'][0]['id'] == create_dialectic_response['dialecticId']
