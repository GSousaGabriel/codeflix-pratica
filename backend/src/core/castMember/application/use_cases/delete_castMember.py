from dataclasses import dataclass
from uuid import UUID
from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.castMember.application.use_cases.exceptions import CastMemberNotFound

class DeleteCastMember:
    def __init__(self, repo = CastMemberRepository):
        self.repo = repo
        
    @dataclass
    class Input:
        id: UUID
    
    def execute(self, input: Input)-> None:
        cast_member = self.repo.get_by_id(input.id)
        
        if cast_member is None:
            raise CastMemberNotFound(f"Cast member with id {input.id} was not found!")
        
        self.repo.delete(cast_member.id)