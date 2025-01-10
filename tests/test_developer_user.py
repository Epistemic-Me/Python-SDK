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

def test_create_developer(mock_grpc_client):
    mock_response = epistemic_me_pb2.CreateDeveloperResponse()
    mock_response.developer.id = 'dev123'
    mock_response.developer.name = 'Test Developer'
    mock_response.developer.email = 'test@example.com'
    mock_response.developer.api_keys.append('test_api_key')
    mock_grpc_client.stub.CreateDeveloper.return_value = mock_response

    result = mock_grpc_client.create_developer(
        name='Test Developer',
        email='test@example.com'
    )
    
    mock_grpc_client.stub.CreateDeveloper.assert_called_once_with(
        epistemic_me_pb2.CreateDeveloperRequest(
            name='Test Developer',
            email='test@example.com'
        ),
        metadata=[('x-api-key', 'test_api_key')]
    )
    assert isinstance(result, dict)
    assert result['id'] == 'dev123'
    assert result['name'] == 'Test Developer'
    assert result['email'] == 'test@example.com'
    assert 'test_api_key' in result['apiKeys']

def test_retrieve_developer(mock_grpc_client):
    mock_response = epistemic_me_pb2.GetDeveloperResponse()
    mock_response.developer.id = 'dev123'
    mock_response.developer.name = 'Test Developer'
    mock_response.developer.email = 'test@example.com'
    mock_response.developer.api_keys.append('test_api_key')
    mock_grpc_client.stub.GetDeveloper.return_value = mock_response

    result = mock_grpc_client.get_developer(id='dev123')
    
    mock_grpc_client.stub.GetDeveloper.assert_called_once_with(
        epistemic_me_pb2.GetDeveloperRequest(id='dev123'),
        metadata=[('x-api-key', 'test_api_key')]
    )
    assert isinstance(result, dict)
    assert result['id'] == 'dev123'
    assert result['name'] == 'Test Developer'
    assert result['email'] == 'test@example.com'
    assert 'test_api_key' in result['apiKeys']

def test_create_user(mock_grpc_client):
    mock_response = epistemic_me_pb2.CreateUserResponse()
    mock_response.user.id = 'user123'
    mock_response.user.developer_id = 'dev123'
    mock_response.user.name = 'Test User'
    mock_response.user.email = 'testuser@example.com'
    mock_grpc_client.stub.CreateUser.return_value = mock_response

    result = mock_grpc_client.create_user(
        developer_id='dev123',
        name='Test User',
        email='testuser@example.com'
    )
    
    mock_grpc_client.stub.CreateUser.assert_called_once_with(
        epistemic_me_pb2.CreateUserRequest(
            developer_id='dev123',
            name='Test User',
            email='testuser@example.com'
        ),
        metadata=[('x-api-key', 'test_api_key')]
    )
    assert isinstance(result, dict)
    assert result['id'] == 'user123'
    assert result['developerId'] == 'dev123'
    assert result['name'] == 'Test User'
    assert result['email'] == 'testuser@example.com'