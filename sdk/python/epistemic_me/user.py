from . import config

class User:
    @classmethod
    def create(cls, developer_id: str, name: str, email: str):
        return config.grpc_client.create_user(developer_id, name, email)

    @classmethod
    def retrieve(cls, user_id: str):
        return config.grpc_client.get_user(user_id)

    @classmethod
    def list(cls, developer_id: str):
        return config.grpc_client.list_users(developer_id)

    @classmethod
    def update(cls, user_id: str, **kwargs):
        return config.grpc_client.update_user(user_id, **kwargs)

    @classmethod
    def delete(cls, user_id: str):
        return config.grpc_client.delete_user(user_id)
