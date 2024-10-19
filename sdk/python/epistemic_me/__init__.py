# from .self_agent import SelfAgent
from .generated.proto import *
from .philosophy import Philosophy
from .dialectic import Dialectic
from .config import Config

class EpistemicMe:
    def __init__(self, api_key: str, base_url: str = "http://localhost:8080"):
        self.config = Config(api_key, base_url)
        # self.self_agent = SelfAgent(self.config)
        self.philosophy = Philosophy(self.config)
        self.dialectic = Dialectic(self.config)

# Convenience function to create an instance
def create(api_key: str, base_url: str = "http://localhost:8080") -> EpistemicMe:
    return EpistemicMe(api_key, base_url)
