import pytest
from src.core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.models import Category as CategoryModel

@pytest.mark.django_db
class TestSave:
    def test_save_category_in_database(self):
        category = Category(name= "Movie", description = "Movie category")
        repo = DjangoORMCategoryRepository()
        
        assert CategoryModel.objects.count() == 0
        repo.save(category)
        assert CategoryModel.objects.count() == 1
        
        category_db = CategoryModel.objects.get()
        assert category_db.id  == category.id
        assert category_db.name == category.name
        assert category_db.description == category.description
        assert category_db.is_active == category.is_active
        
    def test_update_category_in_database(self):
        category = Category(name= "Movie", description = "Movie category")
        repo = DjangoORMCategoryRepository()
        CategoryModel.objects.create(
            id = category.id,
            name = category.name,
            description = category.description,
            is_active = category.is_active
        )
        
        category.name = "Serie"
        category.description = "Serie category"
        
        repo.update(category)
        
        category_db = CategoryModel.objects.get()
        assert category_db.name == "Serie"
        assert category_db.description == "Serie category"
        
    def test_get_category_by_id_in_database(self):
        category = Category(name= "Movie", description = "Movie category")
        repo = DjangoORMCategoryRepository()
        CategoryModel.objects.create(
            id = category.id,
            name = category.name,
            description = category.description,
            is_active = category.is_active
        )
        
        response = repo.get_by_id(category.id)
        
        assert response is not None
        assert response.id == category.id
        assert response.name == category.name
        assert response.description == category.description
        assert response.is_active == category.is_active
        
    def test_get_category_by_id_in_database(self):
        category = Category(name= "Movie", description = "Movie category")
        repo = DjangoORMCategoryRepository()
        CategoryModel.objects.create(
            id = category.id,
            name = category.name,
            description = category.description,
            is_active = category.is_active
        )
        
        repo.delete(category.id)
        assert CategoryModel.objects.count() == 0
                