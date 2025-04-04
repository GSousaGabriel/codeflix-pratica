from unittest.mock import create_autospec
import uuid
import pytest
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.delete_repository import DeleteCategory, DeleteCategoryRequest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category

class TestDeleteCategory:
    def test_delete_category_from_repository(self):
        category = Category(name="Movie", description="Category description")
        mock_repo = create_autospec(CategoryRepository)
        mock_repo.get_by_id.return_value = category
        use_case = DeleteCategory(mock_repo)
        use_case.execute(DeleteCategoryRequest(category.id))
        
        mock_repo.delete.assert_called_once_with(category.id)

    def test_when_category_not_found(self):
        mock_repo = create_autospec(CategoryRepository)
        mock_repo.get_by_id.return_value = None
        use_case = DeleteCategory(mock_repo)
        
        with pytest.raises(CategoryNotFound) as exec_info:
            use_case.execute(DeleteCategoryRequest(uuid.uuid4()))
        
        mock_repo.delete.assert_not_called()
        assert mock_repo.delete.called is False
        