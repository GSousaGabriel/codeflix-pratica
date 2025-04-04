from unittest.mock import MagicMock
from uuid import UUID
import pytest
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryRequest, CreateCategoryResponse, InvalidCategoryData

class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        mock_repo = MagicMock(CategoryRepository)
        use_case = CreateCategory(mock_repo)
        request = CreateCategoryRequest(
            name="Movie",
            description="Movies categories",
            is_active=True
        )
        
        response = use_case.execute(request)
        
        assert response is not None
        assert isinstance(response, CreateCategoryResponse)
        assert isinstance(response.id, UUID)
        assert mock_repo.save.called
        
    def test_create_category_invalid_data(self):
        mock_repo = MagicMock(CategoryRepository)
        use_case = CreateCategory(mock_repo)
        request = CreateCategoryRequest(name="")
        
        with pytest.raises(InvalidCategoryData, match="Name should not be empty") as exec_info:
            use_case.execute(request)
            
        assert exec_info.type is InvalidCategoryData
        assert str(exec_info.value) == "Name should not be empty"
        assert not mock_repo.save.called