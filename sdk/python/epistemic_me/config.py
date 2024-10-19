from .grpc_client import GrpcClient

class Config:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.grpc_client = GrpcClient(base_url)

