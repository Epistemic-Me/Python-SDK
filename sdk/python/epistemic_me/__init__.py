# from .self_model import SelfModel
from .generated.proto import *
from .philosophy import Philosophy
from .dialectic import Dialectic
from .config import Config

class EpistemicMe:
    def __init__(self, api_key: str, base_url: str = "http://localhost:8080"):
        self.config = Config(api_key, base_url)
        # self.self_model = SelfModel(self.config)
        self.philosophy = Philosophy(self.config)
        self.dialectic = Dialectic(self.config)

# Convenience function to create an instance
def create(api_key: str, base_url: str = "http://localhost:8080") -> EpistemicMe:
    return EpistemicMe(api_key, base_url)
