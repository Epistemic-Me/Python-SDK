from . import config

class SelfModel:
    @classmethod
    def create(cls, id: str, philosophies: list[str] = ["default"]):
        return config.grpc_client.create_self_model(id, philosophies)

    @classmethod
    def retrieve(cls, id: str):
        return config.grpc_client.get_self_model(id)

    @classmethod
    def retrieve_belief_system(cls, id: str):
        return config.grpc_client.get_belief_system(id)

    @classmethod
    def list_dialectics(cls, id: str):
        return config.grpc_client.list_dialectics(id)
