from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import InvalidCategoryData
from src.core.category.domain.category import Category

@dataclass
class CreateCategoryRequest:
    name: str
    description: str = ""
    is_active: bool = True
    
@dataclass
class CreateCategoryResponse:
    id: UUID

class CreateCategory:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo
    
    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        try:
            category = Category(name=request.name, description=request.description, is_active=request.is_active)
        except ValueError as err:
            raise InvalidCategoryData(err)
        
        self.repo.save(category=category)
        return CreateCategoryResponse(category.id)