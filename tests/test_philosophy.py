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

def test_create_philosophy(mock_grpc_client):
    mock_response = epistemic_me_pb2.CreatePhilosophyResponse()
    mock_response.philosophy.id = 'phil_001'
    mock_response.philosophy.description = 'Test philosophy text'
    mock_grpc_client.stub.CreatePhilosophy.return_value = mock_response

    request = epistemic_me_pb2.CreatePhilosophyRequest()
    request.description = 'Test philosophy text'
    request.extrapolate_contexts = False
    
    result = mock_grpc_client.stub.CreatePhilosophy(
        request,
        metadata=[('x-api-key', 'test_api_key')]
    )
    
    assert isinstance(result.philosophy.id, str)
    assert result.philosophy.id == 'phil_001'
    assert result.philosophy.description == 'Test philosophy text'

def test_update_philosophy(mock_grpc_client):
    mock_response = epistemic_me_pb2.UpdatePhilosophyResponse()
    mock_response.philosophy.id = 'phil_001'
    mock_response.philosophy.description = 'Updated philosophy text'
    mock_response.philosophy.extrapolate_contexts = True
    mock_grpc_client.stub.UpdatePhilosophy.return_value = mock_response

    request = epistemic_me_pb2.UpdatePhilosophyRequest()
    request.philosophy_id = 'phil_001'
    request.description = 'Updated philosophy text'
    request.extrapolate_contexts = True

    result = mock_grpc_client.stub.UpdatePhilosophy(
        request,
        metadata=[('x-api-key', 'test_api_key')]
    )

    assert isinstance(result.philosophy.id, str)
    assert result.philosophy.id == 'phil_001'
    assert result.philosophy.description == 'Updated philosophy text'
    assert result.philosophy.extrapolate_contexts is True

def test_add_to_self_model(mock_grpc_client):
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
