import epistemic_me
from epistemic_me.models import DialecticType, BeliefType

def main():
    """
    Demonstrates basic usage of the Epistemic Me Python SDK.
    """
    # Initialize the client
    epistemic_me.api_key = "your-api-key"

    try:
        # Create a belief
        belief = epistemic_me.Belief.create(
            user_id="user123",
            content="Regular exercise improves mental clarity",
            belief_type=BeliefType.STATEMENT
        )
        print(f"Created belief: {belief.id}")

        # Create a dialectic
        dialectic = epistemic_me.Dialectic.create(
            self_model_id="user123",
            dialectic_type=DialecticType.DEFAULT
        )
        print(f"Created dialectic: {dialectic.id}")

        # Update dialectic with a question-answer interaction
        update_resp = dialectic.update(
            question="How often do you exercise?",
            answer="I exercise three times a week"
        )
        print("Updated dialectic with Q&A")

        # Retrieve belief system
        belief_system = epistemic_me.SelfModel.retrieve_belief_system(
            id="user123",
            current_observation_context_ids=[]
        )
        print("Retrieved belief system:", belief_system)

    except epistemic_me.APIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 