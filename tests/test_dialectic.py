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

def test_create_dialectic(mock_grpc_client):
    mock_response = epistemic_me_pb2.CreateDialecticResponse()
    mock_response.dialectic.id = 'dialectic_001'
    mock_response.dialectic.self_model_id = 'self_001'
    mock_grpc_client.stub.CreateDialectic.return_value = mock_response

    result = mock_grpc_client.create_dialectic('self_001')
    
    request = epistemic_me_pb2.CreateDialecticRequest()
    request.self_model_id = 'self_001'
    
    mock_grpc_client.stub.CreateDialectic.assert_called_once_with(
        request,
        metadata=[('x-api-key', 'test_api_key')]
    )
    assert isinstance(result, dict)
    assert result['dialectic']['id'] == 'dialectic_001'
    assert result['dialectic']['selfModelId'] == 'self_001'

def test_answer_dialectic(mock_grpc_client):
    mock_response = epistemic_me_pb2.UpdateDialecticResponse()
    mock_response.dialectic.id = 'dialectic_001'
    mock_grpc_client.stub.UpdateDialectic.return_value = mock_response

    # Create UserAnswer message first
    user_answer = dialectic_pb2.UserAnswer()
    user_answer.user_answer = 'Test answer'

    # Create the request and set the UserAnswer
    request = epistemic_me_pb2.UpdateDialecticRequest()
    request.id = 'dialectic_001'
    request.answer.CopyFrom(user_answer)
    
    result = mock_grpc_client.update_dialectic(request.id, user_answer)
    
    mock_grpc_client.stub.UpdateDialectic.assert_called_once_with(
        request,
        metadata=[('x-api-key', 'test_api_key')]
    )
    assert isinstance(result, dict)
    assert result['dialectic']['id'] == 'dialectic_001'
