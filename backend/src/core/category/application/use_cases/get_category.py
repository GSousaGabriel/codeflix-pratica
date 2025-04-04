from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound

@dataclass
class GetCategoryRequest:
    id: UUID
    
@dataclass
class GetCategoryResponse:
    id: UUID
    name: str
    description: str
    is_active: bool

class GetCategory:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo
    
    def execute(self, request: GetCategoryRequest) -> GetCategoryResponse | None:
        category = self.repo.get_by_id(id=request.id)
        
        if category:
            return GetCategoryResponse(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active
            )
        else:
            raise CategoryNotFound(f"Category with id {request.id} not found!")