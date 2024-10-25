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
        self.pb = epistemic_me_pb2

    def _get_metadata(self):
        return [('api-key', self.api_key)]

    def create_belief(self, self_model_id: str, belief_content: str) -> Dict[str, Any]:
        request = self.pb.CreateBeliefRequest(
            self_model_id=self_model_id,
            belief_content=belief_content
        )
        response = self.stub.CreateBelief(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def list_beliefs(self, self_model_id: str) -> List[Dict[str, Any]]:
        request = self.pb.ListBeliefsRequest(self_model_id=self_model_id)
        response = self.stub.ListBeliefs(request, metadata=self._get_metadata())
        return [MessageToDict(belief) for belief in response.beliefs]

    def update_dialectic(self, id: str, answer: dialectic_pb2.UserAnswer, self_model_id: str = "", dry_run: bool = False):
        request = self.pb.UpdateDialecticRequest(
            id=id,
            answer=answer,
            self_model_id=self_model_id,
            dry_run=dry_run
        )
        response = self.stub.UpdateDialectic(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def create_self_model(self, id: str, philosophies: list[str]):
        request = self.pb.CreateSelfModelRequest(id=id, philosophies=philosophies)
        response = self.stub.CreateSelfModel(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def get_self_model(self, id: str):
        request = self.pb.GetSelfModelRequest(self_model_id=id)
        response = self.stub.GetSelfModel(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def get_belief_system(self, id: str) -> Dict[str, Any]:
        request = self.pb.GetBeliefSystemRequest(
            self_model_id=id
        )
        response = self.stub.GetBeliefSystem(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def list_dialectics(self, id: str):
        request = self.pb.ListDialecticsRequest(self_model_id=id)
        response = self.stub.ListDialectics(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def add_philosophy(self, id: str, philosophy_id: str) -> Dict[str, Any]:
        request = self.pb.AddPhilosophyRequest(
            self_model_id=id,
            philosophy_id=philosophy_id
        )
        response = self.stub.AddPhilosophy(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def create_dialectic(self, id: str):
        request = self.pb.CreateDialecticRequest(
            self_model_id=id
        )
        response = self.stub.CreateDialectic(request, metadata=self._get_metadata())
        return MessageToDict(response)

    def create_developer(self, name: str, email: str) -> dict:
        request = self.pb.CreateDeveloperRequest(name=name, email=email)
        response = self.stub.CreateDeveloper(request, metadata=self._get_metadata())
        return MessageToDict(response.developer)

    def get_developer(self, id: str) -> dict:
        request = self.pb.GetDeveloperRequest(id=id)
        response = self.stub.GetDeveloper(request, metadata=self._get_metadata())
        return MessageToDict(response.developer)

    def create_user(self, developer_id: str, name: str, email: str) -> dict:
        request = self.pb.CreateUserRequest(developer_id=developer_id, name=name, email=email)
        response = self.stub.CreateUser(request, metadata=self._get_metadata())
        return MessageToDict(response.user)
