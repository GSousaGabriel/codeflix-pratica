from dataclasses import dataclass
from uuid import UUID
from src.core._shared.listEntity import ListEntity, ListEntityResponse, ListPaginationInput
from src.core.category.application.use_cases.category_repository import CategoryRepository

@dataclass
class CategoryOutput:
    id: UUID
    name: str
    description: str
    is_active: bool

class ListCategory(ListEntity):
    def __init__(self, repo: CategoryRepository):
        self.repo = repo
    
    def execute(self, input: ListPaginationInput) -> ListEntityResponse[CategoryOutput]:
        categories = self.repo.list()
        sorted_categories = sorted(
                [
                    CategoryOutput(
                        id= category.id,
                        name= category.name,
                        description= category.description,
                        is_active= category.is_active
                    ) for category in categories
                ], key=lambda category: getattr(category, input.order_by)
            )
        
        return self.paginate_data(input.current_page, sorted_categories)