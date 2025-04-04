from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound, InvalidCategoryData

@dataclass
class DeleteCategoryRequest:
    id: UUID

class DeleteCategory:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo
    
    def execute(self, request: DeleteCategoryRequest) -> None:
        category = self.repo.get_by_id(id=request.id)
        
        if category:
            self.repo.delete(request.id)
        else:
            raise CategoryNotFound(f"Category with id {request.id} not found!")