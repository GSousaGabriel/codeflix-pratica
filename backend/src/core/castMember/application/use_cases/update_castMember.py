

from dataclasses import dataclass
from uuid import UUID
from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.castMember.application.use_cases.exceptions import CastMemberNotFound, InvalidCastMember
from src.core.castMember.domain.castMember import CastMemberTypeEnum

class UpdateCastMember:
    def __init__(self, repo = CastMemberRepository):
        self.repo = repo
        
    @dataclass
    class Input:
        id: UUID
        type: CastMemberTypeEnum
        name: str = None
        
    def execute(self, input: Input)-> None:
        cast_member = self.repo.get_by_id(input.id)
        
        if cast_member is None:
            raise CastMemberNotFound(f"Cast member with id {input.id} was not found!")
        
        try:
            if input.name is not None:
                cast_member.change_name(input.name)
            
            if input.type:
                cast_member.change_type(input.type)
        except ValueError as e:
            raise InvalidCastMember(e)
        
        self.repo.update(cast_member)
            
        