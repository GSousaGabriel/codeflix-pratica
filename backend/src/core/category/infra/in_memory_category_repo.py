from uuid import UUID

from src.core.category.domain.category import Category


class InMemoryCategoryRepo:
    def __init__(self, categories=None):
        self.categories = categories or []
        
    def save(self, category):
        self.categories.append(category)
        
    def get_by_id(self, id: UUID) -> Category | None:
        return next((category for category in self.categories if category.id == id), None)
        
    def delete(self, id: UUID) -> None:
        category = self.get_by_id(id)
        self.categories.remove(category)
        
    def update(self, category: Category) -> None:
        od_category = self.get_by_id(category.id)
        
        if category:
            self.categories.remove(od_category)
            self.categories.append(category)
        
    def list(self) -> list[Category]:
        return [category for category in self.categories]