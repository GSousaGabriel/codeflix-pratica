import uuid
import pytest
from src.core.category.application.use_cases.delete_repository import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repo import InMemoryCategoryRepo

class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category_movie = Category(name="Movie", description="Movie category")
        category_serie = Category(name="Serie", description="Serie category")
        repo = InMemoryCategoryRepo(categories=[category_movie, category_serie])
        use_case = DeleteCategory(repo)
        request = DeleteCategoryRequest(id=category_movie.id)
        
        response = use_case.execute(request)
        
        assert response is None
        assert repo.get_by_id(category_movie.id) is None
        assert len(repo.categories) == 1

    def test_when_category_not_found(self):
        category_movie = Category(name="Movie", description="Movie category")
        category_serie = Category(name="Serie", description="Serie category")
        repo = InMemoryCategoryRepo(categories=[category_movie, category_serie])
        use_case = DeleteCategory(repo)
        request = DeleteCategoryRequest(id=uuid.uuid4())
        
        with pytest.raises(CategoryNotFound) as exec_info:
            use_case.execute(request)
            
        assert exec_info.type is CategoryNotFound
        assert repo.get_by_id(category_movie.id) is not None
        assert len(repo.categories) == 2
        