from uuid import UUID
from src.core.castMember.domain.castMember import CastMember

class InMemoryCastMemberRepo:
    def __init__(self, cast_members=None):
        self.cast_members = cast_members or []
        
    def save(self, cast_member: CastMember)-> None:
        self.cast_members.append(cast_member)
        
    def get_by_id(self, id: UUID) -> CastMember | None:
        return next((cast_member for cast_member in self.cast_members if cast_member.id == id), None)
    
    def delete(self, id: UUID)-> None:
        cast_member = self.get_by_id(id)
        self.cast_members.remove(cast_member)
        
    def list(self)->list[CastMember]:
        return [cast_member for cast_member in self.cast_members]
    
    def update(self, cast_member: CastMember)-> None:
        old_cast_member  = self.get_by_id(cast_member.id)
        
        if old_cast_member:
            self.cast_members.remove(old_cast_member)
            self.cast_members.append(cast_member)