from .config import Config

config = Config()

def set_api_key(key: str):
    config.api_key = key

def set_base_url(url: str):
    config.base_url = url

# Import these after setting up config to avoid circular imports
from .self_model import SelfModel
from .philosophy import Philosophy
from .dialectic import Dialectic
from .developer import Developer
from .user import User

def create(api_key: str, base_url: str = "http://localhost:8080"):
    set_api_key(api_key)
    set_base_url(base_url)
    return {
        "self_model": SelfModel,
        "philosophy": Philosophy,
        "dialectic": Dialectic,
        "developer": Developer,
        "user": User
    }
