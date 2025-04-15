

from dataclasses import dataclass
from uuid import UUID
from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.castMember.application.use_cases.exceptions import InvalidCastMember
from src.core.castMember.domain.castMember import CastMember, CastMemberTypeEnum

class CreateCastMember:
    def __init__(self, repo: CastMemberRepository):
        self.repo = repo
    
    @dataclass
    class Input:
        name: str
        type: CastMemberTypeEnum
        
    @dataclass
    class Output:
        id: str
        
    def execute(self, input: Input) -> Output:
        try:
            cast_member = CastMember(name=input.name, type=input.type)
        except ValueError as e:
            raise InvalidCastMember(str(e))
        
        self.repo.save(cast_member)
        return self.Output(cast_member.id)