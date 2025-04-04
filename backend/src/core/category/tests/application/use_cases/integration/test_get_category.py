import uuid
import pytest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repo import InMemoryCategoryRepo

class TestGetCategory:
    def test_get_category_with_by_id(self):
        category_movie = Category(name="Movie", description="Movie category")
        category_serie = Category(name="Serie", description="Serie category")
        repo = InMemoryCategoryRepo(categories=[category_movie, category_serie])
        use_case = GetCategory(repo)
        request = GetCategoryRequest(id=category_movie.id)
        
        response = use_case.execute(request)
        
        assert response is not None
        assert isinstance(response, GetCategoryResponse)
        assert response == GetCategoryResponse(
            id=category_movie.id,
            name=category_movie.name,
            description=category_movie.description,
            is_active=category_movie.is_active
        )
        
    def test_create_category_invalid_id(self):
        category_movie = Category(name="Movie", description="Movie category")
        category_serie = Category(name="Serie", description="Serie category")
        repo = InMemoryCategoryRepo(categories=[category_movie, category_serie])
        use_case = GetCategory(repo)
        request = GetCategoryRequest(id=uuid.uuid4())
        
        with pytest.raises(CategoryNotFound) as exec_info:
            use_case.execute(request)
            
        assert exec_info.type is CategoryNotFound
