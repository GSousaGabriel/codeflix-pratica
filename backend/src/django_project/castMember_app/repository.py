from uuid import UUID
from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from django_project.castMember_app.models import CastMember as CastMemberModel
from src.core.castMember.domain.castMember import CastMember

class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, castMember_model: CastMemberModel = CastMemberModel):
        self.castMember_model = castMember_model
        
    def save(self, castMember: CastMember) -> None:
        self.castMember_model.objects.create(
            id = castMember.id,
            name = castMember.name,
            type = castMember.type
        )
        
    def update(self, castMember: CastMember) -> None:
        try:
            self.castMember_model.objects.get(pk=castMember.id)
        except self.castMember_model.DoesNotExist:
            return None
        
        self.castMember_model.objects.filter(pk=castMember.id).update(
            name = castMember.name,
            type = castMember.type
        )
        
    def list(self) -> list[CastMember]:
        return [CastMember(
            id = castMember.id,
            name = castMember.name,
            type = castMember.type
        ) for castMember in self.castMember_model.objects.all()]
        
    def get_by_id(self, id: UUID) -> CastMember:
        try:
            castMember = self.castMember_model.objects.get(pk=id)
            return CastMember(
                id = castMember.id,
                name = castMember.name,
                type = castMember.type
            )
        except self.castMember_model.DoesNotExist:
            return None
            
        
    def delete(self, id: UUID) -> None:
        self.castMember_model.objects.filter(pk=id).delete()