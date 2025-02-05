import uuid
import pytest
import epistemic_me
from epistemic_me.dialectic import LearningObjective
from epistemic_me.generated.proto.models import beliefs_pb2

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
    
    # Test initial dialectic structure
    assert "id" in dialectic
    assert dialectic["id"].startswith("di_")
    assert "agent" in dialectic
    assert dialectic["agent"]["agentType"] == "AGENT_TYPE_GPT_LATEST"
    assert "userInteractions" in dialectic
    
    # Provide an answer and get next question
    updated_dialectic_response = epistemic_me.Dialectic.update(
        id=dialectic["id"],
        answer="I believe regular exercise is important for maintaining health",
        self_model_id=authenticated_client["self_model_id"]
    )
    updated_dialectic = updated_dialectic_response["dialectic"]

    # Test user interactions array
    assert "userInteractions" in updated_dialectic
    user_interactions = updated_dialectic["userInteractions"]
    assert len(user_interactions) == 2  # Original question + next question
    
    # Test first interaction (answered)
    answered_interaction = user_interactions[0]
    assert answered_interaction["status"] == "ANSWERED"
    assert answered_interaction["type"] == "QUESTION_ANSWER"
    
    # Test interaction structure
    assert "interaction" in answered_interaction
    qa = answered_interaction["interaction"]
    assert "questionAnswer" in qa
    question_answer = qa["questionAnswer"]
    assert "question" in question_answer
    assert "answer" in question_answer
    
    # Test extracted beliefs if present
    if "extractedBeliefs" in question_answer:
        beliefs = question_answer["extractedBeliefs"]
        assert isinstance(beliefs, list)
        if len(beliefs) > 0:
            belief = beliefs[0]
            assert "id" in belief
            assert "content" in belief
            assert isinstance(belief["content"], list)
            assert "rawStr" in belief["content"][0]
            assert "type" in belief
    
    # Test next interaction (pending)
    pending_interaction = user_interactions[1]
    assert pending_interaction["status"] == "PENDING_ANSWER"
    assert pending_interaction["type"] == "QUESTION_ANSWER"
    assert "interaction" in pending_interaction
    assert "questionAnswer" in pending_interaction["interaction"]
    
    # Test pending question structure
    pending_question = pending_interaction["interaction"]["questionAnswer"]["question"]
    assert isinstance(pending_question["question"], str)
    assert "createdAtMillisUtc" in pending_question
    
    # Test prediction context if present
    if "predictionContext" in pending_interaction:
        prediction = pending_interaction["predictionContext"]
        assert isinstance(prediction, dict)

def test_create_dialectic_with_learning_objective(authenticated_client):
    # Create a learning objective focused on health beliefs
    learning_objective = LearningObjective(
        description="Learn about user's health and fitness beliefs",
        topics=["health", "fitness", "exercise", "nutrition"],
        target_belief_type=beliefs_pb2.BeliefType.FALSIFIABLE
    )

    dialectic_response = epistemic_me.Dialectic.create(
        self_model_id=authenticated_client["self_model_id"],
        learning_objective=learning_objective
    )
    dialectic = dialectic_response["dialectic"]
    
    # Test basic dialectic structure
    assert "id" in dialectic
    assert "agent" in dialectic
    assert dialectic["agent"]["agentType"] == "AGENT_TYPE_GPT_LATEST"
    
    # Test learning objective was included
    assert "learningObjective" in dialectic
    assert dialectic["learningObjective"]["description"] == "Learn about user's health and fitness beliefs"
    assert all(topic in dialectic["learningObjective"]["topics"] for topic in ["health", "fitness", "exercise", "nutrition"])
    assert dialectic["learningObjective"]["targetBeliefType"] == "FALSIFIABLE"