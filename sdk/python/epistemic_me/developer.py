from . import config

class Developer:
    @classmethod
    def create(cls, name: str, email: str):
        return config.grpc_client.create_developer(name, email)

    @classmethod
    def retrieve(cls, developer_id: str):
        return config.grpc_client.get_developer(developer_id)

    @classmethod
    def list(cls):
        return config.grpc_client.list_developers()

    @classmethod
    def update(cls, developer_id: str, **kwargs):
        return config.grpc_client.update_developer(developer_id, **kwargs)

    @classmethod
    def delete(cls, developer_id: str):
        return config.grpc_client.delete_developer(developer_id)
