from dataclasses import dataclass
from uuid import UUID
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound


@dataclass
class UpdateCategoryRequest:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None

class UpdateCategory:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo
        
    def execute(self, request: UpdateCategoryRequest):
        category = self.repo.get_by_id(request.id)
        
        if category is None:
            raise CategoryNotFound(f"Category with {request.id} not found!")
        
        try:
            if request.is_active is True:
                category.activate()

            if request.is_active is False:
                category.deactivate()

            current_name = category.name
            current_description = category.description

            if request.name is not None:
                current_name = request.name

            if request.description is not None:
                current_description = request.description

            category.update_category(name=current_name, description=current_description)
        except ValueError as error:
            raise ValueError(error)
            
        category.update_category(current_name, current_description)
        self.repo.update(category)