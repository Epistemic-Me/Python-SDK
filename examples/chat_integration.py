import epistemic_me
from epistemic_me.models import DialecticType

def process_chat_conversation(self_model_id: str, conversation: list[dict]):
    """
    Process a chat conversation to build a belief system.
    
    Args:
        self_model_id: ID of the self model
        conversation: List of message dictionaries with 'role' and 'content' keys
    """
    # Create initial dialectic
    dialectic = epistemic_me.Dialectic.create(
        self_model_id=self_model_id,
        dialectic_type=DialecticType.DEFAULT
    )

    # Track created beliefs during the conversation
    created_beliefs = []
    last_dialectic_belief_system = None

    # Process messages and create question/answer pairs
    for message in conversation:
        update_req = {
            "id": dialectic.id,
            "self_model_id": self_model_id
        }

        if message["role"] == "assistant":
            update_req["question_blob"] = message["content"]
        else:
            update_req["answer_blob"] = message["content"]

        # Update the dialectic
        update_resp = dialectic.update(**update_req)

        # Track beliefs from the response
        if update_resp and update_resp.belief_system:
            for belief in update_resp.belief_system.beliefs:
                if belief and belief.id:
                    created_beliefs.append(belief.id)
            last_dialectic_belief_system = update_resp.belief_system

    return created_beliefs, last_dialectic_belief_system

# Example usage
if __name__ == "__main__":
    epistemic_me.api_key = "your-api-key"

    conversation = [
        {"role": "assistant", "content": "How would you describe your sleep habits?"},
        {"role": "user", "content": "I usually get about 8 hours of sleep per night"},
        {"role": "assistant", "content": "What time do you typically go to bed?"},
        {"role": "user", "content": "Around 10:30 PM most nights"}
    ]

    beliefs, belief_system = process_chat_conversation(
        self_model_id="user123",
        conversation=conversation
    )

    print(f"Created beliefs: {beliefs}")
    print(f"Final belief system: {belief_system}") 