from unittest.mock import MagicMock
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.update_category import UpdateCategory, UpdateCategoryRequest
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_name(self):
        category = Category(name="Movie", description="Movie category")
        mock_repo = MagicMock(CategoryRepository)
        mock_repo.get_by_id.return_value = category
        use_case = UpdateCategory(mock_repo)
        request = UpdateCategoryRequest(id=category.id, name="Serie")
        
        use_case.execute(request)
        
        mock_repo.update.assert_called_once_with(category)
        assert category.name == "Serie"
        assert category.description == "Movie category"
    
    def test_update_category_description(self):
        category = Category(name="Movie", description="Movie category")
        mock_repo = MagicMock(CategoryRepository)
        mock_repo.get_by_id.return_value = category
        use_case = UpdateCategory(mock_repo)
        request = UpdateCategoryRequest(id=category.id, description="Serie category")
        
        use_case.execute(request)
        
        mock_repo.update.assert_called_once_with(category)
        assert category.name == "Movie"
        assert category.description == "Serie category"
    
    def test_activate_category(self):
        category = Category(name="Movie", description="Movie category")
        mock_repo = MagicMock(CategoryRepository)
        mock_repo.get_by_id.return_value = category
        use_case = UpdateCategory(mock_repo)
        request = UpdateCategoryRequest(id=category.id, is_active=True)
        
        use_case.execute(request)
        
        mock_repo.update.assert_called_once_with(category)
        assert category.is_active == True
    
    
    def test_deactivate_category(self):
        category = Category(name="Movie", description="Movie category")
        mock_repo = MagicMock(CategoryRepository)
        mock_repo.get_by_id.return_value = category
        use_case = UpdateCategory(mock_repo)
        request = UpdateCategoryRequest(id=category.id, is_active=False)
        
        use_case.execute(request)
        
        mock_repo.update.assert_called_once_with(category)
        assert category.is_active == False