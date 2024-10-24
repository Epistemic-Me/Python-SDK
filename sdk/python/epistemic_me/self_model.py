from . import config

class SelfModel:
    @classmethod
    def create(cls, id: str, philosophies: list[str] = ["default"]):
        return config.grpc_client.create_self_model(id, philosophies)

    @classmethod
    def retrieve(cls, self_id: str):
        return config.grpc_client.get_self_model(self_id)

    @classmethod
    def retrieve_belief_system(cls, self_model_id: str):
        return config.grpc_client.get_belief_system(self_model_id)

    @classmethod
    def list_dialectics(cls, self_model_id: str):
        return config.grpc_client.list_dialectics(self_model_id)
