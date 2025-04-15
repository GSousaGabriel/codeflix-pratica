from dataclasses import dataclass
from uuid import UUID
from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.castMember.domain.castMember import CastMemberTypeEnum

@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberTypeEnum
    
class ListCastMember:
    def __init__(self, repo = CastMemberRepository):
        self.repo = repo
    
    @dataclass
    class Input:
        pass
    
    @dataclass
    class Output:
        data: list[CastMemberOutput]
        
    @dataclass
    class Output:
        data: list[CastMemberOutput] 
        
    def execute(self)->Output:
        return self.Output(
            data = [
                CastMemberOutput(
                id= cast_member.id,
                name= cast_member.name,
                type= cast_member.type)
                for cast_member in self.repo.list()
            ]
        )