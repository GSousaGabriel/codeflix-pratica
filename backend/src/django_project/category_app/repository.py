from uuid import UUID
from src.core.category.application.use_cases.category_repository import CategoryRepository
from django_project.category_app.models import Category as CategoryModel
from src.core.category.domain.category import Category

class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, category_model: CategoryModel = CategoryModel):
        self.category_model = category_model
        
    def save(self, category: Category) -> None:
        category_mapped = CategoryModeMapper.to_model(category)
        category_mapped.save()

    def update(self, category: Category) -> None:
        self.category_model.objects.filter(pk=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
        
    def get_by_id(self, id: UUID)-> Category | None:
        try:
            category = self.category_model.objects.get(pk=id)
            return CategoryModeMapper.to_entity(category)
        except self.category_model.DoesNotExist:
            return None
        
    def delete(self, id: UUID):
        self.category_model.objects.filter(pk=id).delete()
        
    def list(self)-> list[Category]:
        return [CategoryModeMapper.to_entity(category)
            for category in self.category_model.objects.all()]
        
class CategoryModeMapper:
    @staticmethod
    def to_model(category: Category)-> CategoryModel:
        return CategoryModel(
            id = category.id,
            name = category.name,
            description = category.description,
            is_active = category.is_active
        )
        
    @staticmethod
    def to_entity(category_model: CategoryModel) -> Category:
        return Category(
            id = category_model.id,
            name = category_model.name,
            description = category_model.description,
            is_active = category_model.is_active
        )