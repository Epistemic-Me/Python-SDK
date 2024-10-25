import uuid
import pytest
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
    developer_with_key = epistemic_me.Developer.retrieve(id=developer["id"])
    
    # Return both the authenticated client and the developer info for tests that need it
    return {
        "client": epistemic_me.create(developer_with_key["apiKeys"][0], "localhost:8080"),
        "developer": developer_with_key
    }

def test_create_developer(client):
    developer_name = f"Test Developer {uuid.uuid4()}"
    developer_email = f"test_{uuid.uuid4()}@example.com"
    developer = epistemic_me.Developer.create(name=developer_name, email=developer_email)
    assert "id" in developer
    assert "name" in developer
    assert "email" in developer
    assert "apiKeys" in developer
    assert "createdAt" in developer
    assert "updatedAt" in developer
    assert developer["name"] == developer_name
    assert developer["email"] == developer_email

def test_retrieve_developer(authenticated_client):
    retrieved_developer = epistemic_me.Developer.retrieve(
        id=authenticated_client["developer"]["id"]
    )
    assert retrieved_developer["id"] == authenticated_client["developer"]["id"]
    assert retrieved_developer["name"] == authenticated_client["developer"]["name"]
    assert retrieved_developer["email"] == authenticated_client["developer"]["email"]

def test_create_user(authenticated_client):
    user_name = f"Test User {uuid.uuid4()}"
    user_email = f"test_{uuid.uuid4()}@example.com"
    user = epistemic_me.User.create(
        developer_id=authenticated_client["developer"]["id"],
        name=user_name,
        email=user_email
    )
    assert "id" in user
    assert "developerId" in user
    assert "name" in user
    assert "email" in user
    assert "createdAt" in user
    assert "updatedAt" in user
    assert user["developerId"] == authenticated_client["developer"]["id"]
    assert user["name"] == user_name
    assert user["email"] == user_email

