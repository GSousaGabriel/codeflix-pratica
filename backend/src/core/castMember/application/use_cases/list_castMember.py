from dataclasses import dataclass
from uuid import UUID
from src.core._shared.listEntity import ListEntity, ListEntityResponse, ListPaginationInput
from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.castMember.domain.castMember import CastMemberTypeEnum

@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberTypeEnum
    
class ListCastMember(ListEntity):
    def __init__(self, repo = CastMemberRepository):
        self.repo = repo
        
    def execute(self, input: ListPaginationInput)-> ListEntityResponse[CastMemberOutput]:
        castMembers = self.repo.list()
        
        sorted_castMember = sorted(
            [
                CastMemberOutput(
                id= castMember.id,
                name= castMember.name,
                type= castMember.type)
                for castMember in castMembers
            ], key=lambda castMember: getattr(castMember, input.order_by)
        )
        
        return self.paginate_data(input.current_page, sorted_castMember)