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
    
    # Set the API key first
    epistemic_me.config.api_key = developer["apiKeys"][0]
    
    # Create a self model after setting the API key
    self_model = epistemic_me.SelfModel.create(id=str(uuid.uuid4()))

    return {
        "developer": developer,
        "self_model_id": self_model["selfModel"]["id"]
    }

def test_create_dialectic(authenticated_client):
    dialectic_response = epistemic_me.Dialectic.create(
        self_model_id=authenticated_client["self_model_id"]
    )
    dialectic = dialectic_response["dialectic"]
    print(dialectic)
    assert "id" in dialectic
    assert "agent" in dialectic
    assert dialectic["agent"]["agentType"] == "AGENT_TYPE_GPT_LATEST"
    assert len(dialectic["userInteractions"]) == 1

def test_qa_flow(authenticated_client):
    # Create a new dialectic
    dialectic_response = epistemic_me.Dialectic.create(
        self_model_id=authenticated_client["self_model_id"]
    )
    dialectic = dialectic_response["dialectic"]
    
    # Provide an answer and get next question
    updated_dialectic_response = epistemic_me.Dialectic.update(
        id=dialectic["id"],
        answer="I believe regular exercise is important for maintaining health",
        self_model_id=authenticated_client["self_model_id"]
    )
    updated_dialectic = updated_dialectic_response["dialectic"]

    # test for user interactions
    assert "userInteractions" in updated_dialectic
    user_interactions = updated_dialectic["userInteractions"]
    assert len(user_interactions) == 2
    print(user_interactions[0])
    assert user_interactions[0]["status"] == "ANSWERED"
    assert user_interactions[1]["status"] == "PENDING_ANSWER"
