from uuid import UUID
import pytest
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse
from src.core.category.application.use_cases.exceptions import InvalidCategoryData
from src.core.category.infra.in_memory_category_repo import InMemoryCategoryRepo

class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repo = InMemoryCategoryRepo()
        use_case = CreateCategory(repo)
        request = CreateCategoryRequest(
            name="Movie",
            description="Movies categories",
            is_active=True
        )
        
        response = use_case.execute(request)
        
        assert response is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert len(repo.categories) == 1
        
        persisted_category = repo.categories[0]
        assert persisted_category.id == response.id
        assert persisted_category.name == request.name
        assert persisted_category.description == request.description
        assert persisted_category.is_active == request.is_active
        
    def test_create_category_invalid_data(self):
        repo = InMemoryCategoryRepo()
        use_case = CreateCategory(repo)
        request = CreateCategoryRequest(name="")
        
        with pytest.raises(InvalidCategoryData, match="Name should not be empty") as exec_info:
            use_case.execute(request)
            
        assert exec_info.type is InvalidCategoryData
        assert str(exec_info.value) == "Name should not be empty"
        assert len(repo.categories) == 0
