from . import config

class User:
    @classmethod
    def create(cls, developer_id: str, name: str, email: str):
        return config.grpc_client.create_user(developer_id, name, email)

    @classmethod
    def retrieve(cls, id: str):
        return config.grpc_client.get_user(id)

    @classmethod
    def list(cls, developer_id: str):
        return config.grpc_client.list_users(developer_id)

    @classmethod
    def update(cls, id: str, **kwargs):
        return config.grpc_client.update_user(id, **kwargs)

    @classmethod
    def delete(cls, id: str):
        return config.grpc_client.delete_user(id)
