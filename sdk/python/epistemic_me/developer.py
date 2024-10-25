from . import config

class Developer:
    @classmethod
    def create(cls, name: str, email: str):
        return config.grpc_client.create_developer(name, email)

    @classmethod
    def retrieve(cls, id: str):
        return config.grpc_client.get_developer(id)

    @classmethod
    def list(cls):
        return config.grpc_client.list_developers()

    @classmethod
    def update(cls, id: str, **kwargs):
        return config.grpc_client.update_developer(id, **kwargs)

    @classmethod
    def delete(cls, id: str):
        return config.grpc_client.delete_developer(id)
