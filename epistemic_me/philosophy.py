from . import config

class Philosophy:
    @classmethod
    def create(cls, description: str, extrapolate_contexts: bool = False):
        return config.grpc_client.create_philosophy(description, extrapolate_contexts)

    @classmethod
    def update(cls, philosophy_id: str, description: str, extrapolate_contexts: bool = False):
        return config.grpc_client.update_philosophy(philosophy_id, description, extrapolate_contexts)

    @classmethod
    def add_to_self_model(cls, self_model_id: str, philosophy_id: str):
        return config.grpc_client.add_philosophy(self_model_id, philosophy_id)

    @classmethod
    def modify(cls, id: str, self_model_id: str):
        return config.grpc_client.modify_philosophy(id, self_model_id)

    @classmethod
    def add_observation_contexts(cls, id: str, new_observation_contexts: dict):
        return config.grpc_client.add_observation_contexts(id, new_observation_contexts)
