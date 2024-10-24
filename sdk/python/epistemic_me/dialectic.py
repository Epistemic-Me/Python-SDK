from . import config
from .generated.proto.models import dialectic_pb2

class Dialectic:
    @classmethod
    def create(cls, self_model_id: str):
        return config.grpc_client.create_dialectic(self_model_id)

    def answer(self, id: str, answer: str):
        user_answer = dialectic_pb2.UserAnswer(user_answer=answer)
        return config.grpc_client.update_dialectic(config.self_id, id, user_answer)

    # Add other methods as needed
