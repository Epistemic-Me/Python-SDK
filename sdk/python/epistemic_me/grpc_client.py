import grpc
from google.protobuf.json_format import MessageToDict
from typing import List, Dict, Any

from .generated.proto import epistemic_me_pb2, epistemic_me_pb2_grpc
from .generated.proto.models import beliefs_pb2, dialectic_pb2

class GrpcClient:
    def __init__(self, base_url: str):
        self.channel = grpc.insecure_channel(base_url)
        self.stub = epistemic_me_pb2_grpc.EpistemicMeServiceStub(self.channel)

    def create_belief(self, user_id: str, belief_content: str) -> Dict[str, Any]:
        request = epistemic_me_pb2.CreateBeliefRequest(
            user_id=user_id,
            belief_content=belief_content
        )
        response = self.stub.CreateBelief(request)
        return MessageToDict(response)

    def list_beliefs(self, user_id: str) -> List[Dict[str, Any]]:
        request = epistemic_me_pb2.ListBeliefsRequest(user_id=user_id)
        response = self.stub.ListBeliefs(request)
        return [MessageToDict(belief) for belief in response.beliefs]

    def list_dialectics(self, user_id: str) -> List[Dict[str, Any]]:
        request = epistemic_me_pb2.ListDialecticsRequest(user_id=user_id)
        response = self.stub.ListDialectics(request)
        return [MessageToDict(dialectic) for dialectic in response.dialectics]

    def create_dialectic(self, user_id: str, dialectic_type: dialectic_pb2.DialecticType) -> Dict[str, Any]:
        request = epistemic_me_pb2.CreateDialecticRequest(
            user_id=user_id,
            dialectic_type=dialectic_type
        )
        response = self.stub.CreateDialectic(request)
        return MessageToDict(response)

    def update_dialectic(self, user_id: str, dialectic_id: str, answer: dialectic_pb2.UserAnswer) -> Dict[str, Any]:
        request = epistemic_me_pb2.UpdateDialecticRequest(
            user_id=user_id,
            dialectic_id=dialectic_id,
            answer=answer
        )
        response = self.stub.UpdateDialectic(request)
        return MessageToDict(response)

    def get_belief_system_detail(self, user_id: str, current_observation_context_ids: List[str]) -> Dict[str, Any]:
        request = epistemic_me_pb2.GetBeliefSystemDetailRequest(
            user_id=user_id,
            current_observation_context_ids=current_observation_context_ids
        )
        response = self.stub.GetBeliefSystemDetail(request)
        return MessageToDict(response)
