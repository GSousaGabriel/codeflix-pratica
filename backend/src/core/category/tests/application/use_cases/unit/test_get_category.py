from unittest.mock import MagicMock
import uuid
import pytest
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.domain.category import Category

class TestGetCategory:
    def test_get_category_with_by_id(self):
        category = Category(name="Movie", description="Movie category")
        mock_repo = MagicMock(CategoryRepository)
        mock_repo.get_by_id.return_value = category
        use_case = GetCategory(mock_repo)
        request = GetCategoryRequest(id=category.id)
        
        response = use_case.execute(request)
        
        assert response is not None
        assert isinstance(response, GetCategoryResponse)
        assert response == GetCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active
        )
        
    def test_create_category_invalid_id(self):
        mock_repo = MagicMock(CategoryRepository)
        mock_repo.get_by_id.return_value = None
        use_case = GetCategory(mock_repo)
        request = GetCategoryRequest(id=uuid.uuid4())
        
        with pytest.raises(CategoryNotFound) as exec_info:
            use_case.execute(request)
            
        assert exec_info.type is CategoryNotFound
