from .grpc_client import GrpcClient

class Config:
    def __init__(self):
        self._api_key = None
        self._base_url = "http://localhost:8080"
        self._grpc_client = None

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value
        self._update_grpc_client()

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value
        self._update_grpc_client()

    @property
    def grpc_client(self):
        if self._grpc_client is None:
            self._update_grpc_client()
        return self._grpc_client

    def _update_grpc_client(self):
        self._grpc_client = GrpcClient(self._base_url, self._api_key)
