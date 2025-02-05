from . import config
from .generated.proto.models import dialectic_pb2
from .generated.proto.models import beliefs_pb2
from typing import List, Optional

class LearningObjective:
    def __init__(self, description: str, topics: List[str], target_belief_type: beliefs_pb2.BeliefType):
        self.description = description
        self.topics = topics
        self.target_belief_type = target_belief_type

    def to_proto(self) -> dialectic_pb2.LearningObjective:
        return dialectic_pb2.LearningObjective(
            description=self.description,
            topics=self.topics,
            target_belief_type=self.target_belief_type
        )

class Dialectic:
    @classmethod
    def create(cls, self_model_id: str, learning_objective: Optional[LearningObjective] = None, 
               dialectic_type: dialectic_pb2.DialecticType = dialectic_pb2.DialecticType.DEFAULT):
        """Creates a new dialectic session with an optional learning objective"""
        return config.grpc_client.create_dialectic(
            self_model_id, 
            learning_objective=learning_objective,
            dialectic_type=dialectic_type
        )

    @classmethod
    def update(cls, id: str, answer: str, self_model_id: str):
        """Updates an existing dialectic with a user's answer and returns the next question"""
        user_answer = dialectic_pb2.UserAnswer(user_answer=answer)
        return config.grpc_client.update_dialectic(id, user_answer, self_model_id)
