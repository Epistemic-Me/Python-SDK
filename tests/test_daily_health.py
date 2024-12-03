import pytest
from unittest.mock import Mock, patch
from epistemic_me import create
from sdk.python.epistemic_me.self_model import SelfModel
from epistemic_me.dialectic import Dialectic

@pytest.fixture
def mock_self_model():
    config = Mock()
    return SelfModel(config)

@pytest.fixture
def mock_dialectic():
    config = Mock()
    return Dialectic(config)

def test_health_scenario(mock_self_model, mock_dialectic):
    # Step 1: Populate beliefs
    mock_self_model.beliefs = {
        "sleep": {
            "content": "Achieving 7-8 hours of sleep will lead to waking up feeling emotionally rested.",
            "probability": 0.8
        },
        "exercise": {
            "content": "Regular exercise improves overall health and energy levels.",
            "probability": 0.9
        },
        "nutrition": {
            "content": "A balanced diet supports cognitive function and mood stability.",
            "probability": 0.85
        }
    }

    # Step 2: Instantiate a dialectic session
    dialectic_session = mock_dialectic.create(mock_self_model.id)

    # Step 3: Prediction
    prediction = mock_self_model.predict_health_outcome()
    assert "feeling energized and emotionally balanced" in prediction

    # Step 4: Action
    mock_self_model.take_action("Sleep for 8 hours")

    # Step 5: Observation
    observation = mock_self_model.collect_evidence()
    assert "sleep duration" in observation
    assert "emotional state upon waking" in observation

    # Step 6: Compare prediction to evidence
    discrepancy = mock_self_model.compare_prediction_to_evidence(prediction, observation)

    # Step 7: Update beliefs
    updated_beliefs = mock_self_model.update_beliefs(discrepancy)
    assert updated_beliefs["sleep"]["probability"] != mock_self_model.beliefs["sleep"]["probability"]

    # Optional: Trigger another cycle
    new_prediction = mock_self_model.predict_health_outcome()
    assert new_prediction != prediction

# Add more specific test methods for each step of the dialectic cycle
def test_predict_health_outcome(mock_self_model):
    prediction = mock_self_model.predict_health_outcome()
    assert isinstance(prediction, str)
    assert len(prediction) > 0

def test_take_action(mock_self_model):
    action = "Exercise for 30 minutes"
    result = mock_self_model.take_action(action)
    assert result == f"Action taken: {action}"

def test_collect_evidence(mock_self_model):
    evidence = mock_self_model.collect_evidence()
    assert isinstance(evidence, dict)
    assert "sleep duration" in evidence
    assert "emotional state upon waking" in evidence

def test_compare_prediction_to_evidence(mock_self_model):
    prediction = "feeling energized and emotionally balanced"
    evidence = {
        "sleep duration": 7.5,
        "emotional state upon waking": "somewhat rested"
    }
    discrepancy = mock_self_model.compare_prediction_to_evidence(prediction, evidence)
    assert isinstance(discrepancy, float)
    assert 0 <= discrepancy <= 1

def test_update_beliefs(mock_self_model):
    initial_belief = mock_self_model.beliefs["sleep"]["probability"]
    discrepancy = 0.2
    updated_beliefs = mock_self_model.update_beliefs(discrepancy)
    assert updated_beliefs["sleep"]["probability"] != initial_belief
