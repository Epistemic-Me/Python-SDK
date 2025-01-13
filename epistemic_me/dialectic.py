from . import config
from .generated.proto.models import dialectic_pb2

class Dialectic:
    @classmethod
    def create(cls, self_model_id: str):
        """Creates a new dialectic session"""
        return config.grpc_client.create_dialectic(self_model_id)

    @classmethod
    def update(cls, id: str, answer: str, self_model_id: str):
        """Updates an existing dialectic with a user's answer and returns the next question"""
        user_answer = dialectic_pb2.UserAnswer(user_answer=answer)
        return config.grpc_client.update_dialectic(id, user_answer, self_model_id)
