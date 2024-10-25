import pytest
from unittest.mock import Mock, patch
from epistemic_me.grpc_client import GrpcClient
from epistemic_me.generated.proto import epistemic_me_pb2
from epistemic_me.generated.proto.models import dialectic_pb2

@pytest.fixture
def mock_grpc_client():
    with patch('epistemic_me.grpc_client.grpc.insecure_channel') as mock_channel:
        client = GrpcClient('localhost:50051', 'test_api_key')
        client.stub = Mock()
        yield client

def test_create_belief(mock_grpc_client):
    mock_response = epistemic_me_pb2.CreateBeliefResponse()
    mock_grpc_client.stub.CreateBelief.return_value = mock_response

    result = mock_grpc_client.create_belief('self_model123', 'Test belief')
    
    mock_grpc_client.stub.CreateBelief.assert_called_once_with(
        epistemic_me_pb2.CreateBeliefRequest(self_model_id='self_model123', belief_content='Test belief'),
        metadata=[('api-key', 'test_api_key')]
    )
    assert isinstance(result, dict)

def test_list_beliefs(mock_grpc_client):
    mock_response = epistemic_me_pb2.ListBeliefsResponse()
    mock_grpc_client.stub.ListBeliefs.return_value = mock_response

    result = mock_grpc_client.list_beliefs('self_model123')
    
    mock_grpc_client.stub.ListBeliefs.assert_called_once_with(
        epistemic_me_pb2.ListBeliefsRequest(self_model_id='self_model123'),
        metadata=[('api-key', 'test_api_key')]
    )
    assert isinstance(result, list)

def test_create_dialectic(mock_grpc_client):
    mock_response = epistemic_me_pb2.CreateDialecticResponse()
    mock_grpc_client.stub.CreateDialectic.return_value = mock_response

    result = mock_grpc_client.create_dialectic('self_model123')
    
    mock_grpc_client.stub.CreateDialectic.assert_called_once_with(
        epistemic_me_pb2.CreateDialecticRequest(self_model_id='self_model123'),
        metadata=[('api-key', 'test_api_key')]
    )
    assert isinstance(result, dict)

def test_update_dialectic(mock_grpc_client):
    mock_response = epistemic_me_pb2.UpdateDialecticResponse()
    mock_grpc_client.stub.UpdateDialectic.return_value = mock_response
    
    user_answer = dialectic_pb2.UserAnswer(user_answer="Test answer")
    
    result = mock_grpc_client.update_dialectic(
        dialectic_id='dialectic123',
        answer=user_answer,
        self_model_id='model123'
    )
    
    mock_grpc_client.stub.UpdateDialectic.assert_called_once_with(
        epistemic_me_pb2.UpdateDialecticRequest(
            id='dialectic123',
            answer=user_answer,
            self_model_id='model123',
            dry_run=False
        ),
        metadata=[('api-key', 'test_api_key')]
    )
    assert isinstance(result, dict)

def test_get_belief_system(mock_grpc_client):
    mock_response = epistemic_me_pb2.GetBeliefSystemResponse()
    mock_grpc_client.stub.GetBeliefSystem.return_value = mock_response

    result = mock_grpc_client.get_belief_system('self_model123')
    
    mock_grpc_client.stub.GetBeliefSystem.assert_called_once_with(
        epistemic_me_pb2.GetBeliefSystemRequest(
            self_model_id='self_model123'
        ),
        metadata=[('api-key', 'test_api_key')]
    )
    assert isinstance(result, dict)
