import pytest
from unittest.mock import Mock, patch
from epistemic_me.grpc_client import GrpcClient
from epistemic_me.generated.proto import epistemic_me_pb2

@pytest.fixture
def mock_grpc_client():
    with patch('epistemic_me.grpc_client.grpc.insecure_channel') as mock_channel:
        client = GrpcClient('localhost:50051', 'test_api_key')
        client.stub = Mock()
        yield client

def test_create_self_model(mock_grpc_client):
    mock_response = epistemic_me_pb2.CreateSelfModelResponse()
    mock_response.self_model.id = 'self_001'
    mock_response.self_model.philosophies.extend([])
    mock_response.self_model.belief_system.beliefs.extend([])
    mock_grpc_client.stub.CreateSelfModel.return_value = mock_response

    request = epistemic_me_pb2.CreateSelfModelRequest()
    request.id = 'self_001'
    
    result = mock_grpc_client.stub.CreateSelfModel(
        request,
        metadata=[('x-api-key', 'test_api_key')]
    )
    
    assert result.self_model.id == 'self_001'
    assert hasattr(result.self_model, 'philosophies')
    assert hasattr(result.self_model, 'belief_system')

def test_get_self(mock_grpc_client):
    mock_response = epistemic_me_pb2.GetSelfModelResponse()
    mock_response.self_model.id = 'self_001'
    mock_response.self_model.philosophies.extend([])
    mock_response.self_model.belief_system.beliefs.extend([])
    mock_grpc_client.stub.GetSelfModel.return_value = mock_response

    request = epistemic_me_pb2.GetSelfModelRequest()
    request.self_model_id = 'self_001'
    
    result = mock_grpc_client.stub.GetSelfModel(
        request,
        metadata=[('x-api-key', 'test_api_key')]
    )
    
    assert result.self_model.id == 'self_001'
    assert hasattr(result.self_model, 'philosophies')
    assert hasattr(result.self_model, 'belief_system')

def test_add_philosophy(mock_grpc_client):
    mock_response = epistemic_me_pb2.AddPhilosophyResponse()
    mock_response.updated_self_model.id = 'self_001'
    mock_response.updated_self_model.philosophies.append('phil_001')
    mock_grpc_client.stub.AddPhilosophy.return_value = mock_response

    request = epistemic_me_pb2.AddPhilosophyRequest()
    request.self_model_id = 'self_001'
    request.philosophy_id = 'phil_001'
    
    result = mock_grpc_client.stub.AddPhilosophy(
        request,
        metadata=[('x-api-key', 'test_api_key')]
    )
    
    assert isinstance(result.updated_self_model.id, str)
    assert result.updated_self_model.id == 'self_001'
    assert 'phil_001' in result.updated_self_model.philosophies
