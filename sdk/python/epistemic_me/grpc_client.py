import grpc
from google.protobuf.json_format import MessageToDict
from typing import List, Dict, Any

from .generated.proto import epistemic_me_pb2, epistemic_me_pb2_grpc
from .generated.proto.models import dialectic_pb2

class GrpcClient:
    def __init__(self, base_url: str, api_key: str):
        self.channel = grpc.insecure_channel(base_url)
        self.stub = epistemic_me_pb2_grpc.EpistemicMeServiceStub(self.channel)
        self.api_key = api_key

    def _get_metadata(self):
        return [('api-key', self.api_key)]

    def create_belief(self, user_id: str, belief_content: str) -> Dict[str, Any]:
        request = epistemic_me_pb2.CreateBeliefRequest(
            user_id=user_id,
            belief_content=belief_content
        )
        response = self.stub.CreateBelief(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def list_beliefs(self, user_id: str) -> List[Dict[str, Any]]:
        request = epistemic_me_pb2.ListBeliefsRequest(user_id=user_id)
        response = self.stub.ListBeliefs(request, metadata=self._get_metadata())
        return [MessageToDict(belief) for belief in response.beliefs]

    def update_dialectic(self, dialectic_id: str, answer: dialectic_pb2.UserAnswer, self_model_id: str = "", dry_run: bool = False):
        request = epistemic_me_pb2.UpdateDialecticRequest(
            id=dialectic_id,
            answer=answer,
            self_model_id=self_model_id,
            dry_run=dry_run
        )
        response = self.stub.UpdateDialectic(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def create_self_model(self, id: str, philosophies: list[str]):
        request = epistemic_me_pb2.CreateSelfModelRequest(id=id, philosophies=philosophies)
        response = self.stub.CreateSelfModel(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def get_self_model(self, self_id: str):
        request = epistemic_me_pb2.GetSelfModelRequest(self_model_id=self_id)
        response = self.stub.GetSelfModel(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def get_belief_system(self, self_model_id: str) -> Dict[str, Any]:
        request = epistemic_me_pb2.GetBeliefSystemRequest(
            self_model_id=self_model_id
        )
        response = self.stub.GetBeliefSystem(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def list_dialectics(self, self_model_id: str):
        request = epistemic_me_pb2.ListDialecticsRequest(self_model_id=self_model_id)
        response = self.stub.ListDialectics(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def add_philosophy(self, self_model_id: str, philosophy_id: str) -> Dict[str, Any]:
        request = epistemic_me_pb2.AddPhilosophyRequest(
            self_model_id=self_model_id,
            philosophy_id=philosophy_id
        )
        response = self.stub.AddPhilosophy(request)
        return MessageToDict(response)

    def create_dialectic(self, self_model_id: str):
        request = epistemic_me_pb2.CreateDialecticRequest(
            id=self_model_id
        )
        response = self.stub.CreateDialectic(request, metadata=self._get_metadata())
        return MessageToDict(response)
