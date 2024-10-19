import pytest
from unittest.mock import Mock, patch
from epistemic_me.grpc_client import GrpcClient
from epistemic_me.generated.proto import epistemic_me_pb2
from epistemic_me.generated.proto.models import dialectic_pb2

@pytest.fixture
def mock_grpc_client():
    with patch('epistemic_me.grpc_client.grpc.insecure_channel') as mock_channel:
        client = GrpcClient('localhost:50051')
        client.stub = Mock()
        yield client

def test_create_belief(mock_grpc_client):
    mock_response = epistemic_me_pb2.CreateBeliefResponse()
    mock_grpc_client.stub.CreateBelief.return_value = mock_response

    result = mock_grpc_client.create_belief('user123', 'Test belief')
    
    mock_grpc_client.stub.CreateBelief.assert_called_once()
    assert isinstance(result, dict)

def test_list_beliefs(mock_grpc_client):
    mock_response = epistemic_me_pb2.ListBeliefsResponse()
    mock_grpc_client.stub.ListBeliefs.return_value = mock_response

    result = mock_grpc_client.list_beliefs('user123')
    
    mock_grpc_client.stub.ListBeliefs.assert_called_once()
    assert isinstance(result, list)

def test_create_dialectic(mock_grpc_client):
    mock_response = epistemic_me_pb2.CreateDialecticResponse()
    mock_grpc_client.stub.CreateDialectic.return_value = mock_response

    result = mock_grpc_client.create_dialectic('user123', dialectic_pb2.DEFAULT)
    
    mock_grpc_client.stub.CreateDialectic.assert_called_once()
    assert isinstance(result, dict)

def test_update_dialectic(mock_grpc_client):
    mock_response = epistemic_me_pb2.UpdateDialecticResponse()
    mock_grpc_client.stub.UpdateDialectic.return_value = mock_response

    user_answer = dialectic_pb2.UserAnswer(user_answer="Test answer")
    result = mock_grpc_client.update_dialectic('user123', 'dialectic123', user_answer)
    
    mock_grpc_client.stub.UpdateDialectic.assert_called_once()
    assert isinstance(result, dict)

def test_get_belief_system_detail(mock_grpc_client):
    mock_response = epistemic_me_pb2.GetBeliefSystemDetailResponse()
    mock_grpc_client.stub.GetBeliefSystemDetail.return_value = mock_response

    result = mock_grpc_client.get_belief_system_detail('user123', ['context1', 'context2'])
    
    mock_grpc_client.stub.GetBeliefSystemDetail.assert_called_once()
    assert isinstance(result, dict)
