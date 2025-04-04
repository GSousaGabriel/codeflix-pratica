from unittest.mock import MagicMock
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repo import InMemoryCategoryRepo

class TestUpdateCategory:
    def test_update_category_name_and_description(self):
        category_movie = Category(name="Movie", description="Movie category")
        category_serie = Category(name="Serie", description="Serie category")
        repo = InMemoryCategoryRepo(categories=[category_movie, category_serie])
        use_case = UpdateCategory(repo)
        request = UpdateCategoryRequest(id=category_movie.id, name="Animation", description="Animation category")
        
        response = use_case.execute(request)
        updated_category = repo.get_by_id(category_movie.id)
        
        assert response is None
        assert category_movie.name == "Animation"
        assert category_movie.description == "Animation category"
        assert updated_category.name == "Animation"
        assert updated_category.description == "Animation category"
    
    def test_activate_category(self):
        category = Category(name="Movie", description="Movie category")
        repo = InMemoryCategoryRepo(categories=[category])
        use_case = UpdateCategory(repo)
        request = UpdateCategoryRequest(id=category.id, is_active=True)
        
        use_case.execute(request)
        updated_category = repo.get_by_id(category.id)
        
        assert category.is_active == True
        assert updated_category.is_active == True
    
    def test_deactivate_category(self):
        category = Category(name="Movie", description="Movie category")
        repo = InMemoryCategoryRepo(categories=[category])
        use_case = UpdateCategory(repo)
        request = UpdateCategoryRequest(id=category.id, is_active=False)
        
        use_case.execute(request)
        updated_category = repo.get_by_id(category.id)
        
        assert category.is_active == False
        assert updated_category.is_active == False