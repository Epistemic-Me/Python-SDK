from . import config

class Philosophy:
    @classmethod
    def create(cls, self_model_id: str, description: str, observation_contexts: list = None, extrapolate_contexts: bool = False):
        return config.grpc_client.create_philosophy(self_model_id, description, observation_contexts, extrapolate_contexts)

    @classmethod
    def modify(cls, id: str, self_model_id: str):
        return config.grpc_client.modify_philosophy(id, self_model_id)

    @classmethod
    def add_observation_contexts(cls, id: str, new_observation_contexts: dict):
        return config.grpc_client.add_observation_contexts(id, new_observation_contexts)
