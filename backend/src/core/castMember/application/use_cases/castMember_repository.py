
from abc import ABC, abstractmethod
from uuid import UUID

from src.core.castMember.domain.castMember import CastMember

class CastMemberRepository(ABC):
    @abstractmethod
    def save(self, cast_member: CastMember) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> CastMember | None:
        raise NotImplementedError
    
    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def list(self) -> list[CastMember]:
        raise NotImplementedError
    
    @abstractmethod
    def update(self, cast_member: CastMember) -> None:
        raise NotImplementedError