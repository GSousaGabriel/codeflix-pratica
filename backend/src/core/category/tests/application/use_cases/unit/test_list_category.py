from unittest.mock import MagicMock
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import CategoryOutput, ListCategory, ListCategoryResponse, ListCategoryRequest
from src.core.category.domain.category import Category

class TestListCategory:
    def test_return_all_categories(self):
        category_1 = Category(name="Movie")
        category_2 = Category(name="Serie")
        mock_repo = MagicMock(CategoryRepository)
        mock_repo.list.return_value = [category_1, category_2]
        use_case = ListCategory(mock_repo)
        request = ListCategoryRequest()
        
        response = use_case.execute(request)
        
        assert response is not None
        assert len(response.data) == 2
        assert isinstance(response, ListCategoryResponse)
        assert response == ListCategoryResponse(data = [CategoryOutput(
                    id= category.id,
                    name= category.name,
                    description= category.description,
                    is_active= category.is_active
                ) for category in response.data])
        
    def test_return_empty_list(self):
        mock_repo = MagicMock(CategoryRepository)
        mock_repo.get_by_id.return_value = []
        use_case = ListCategory(mock_repo)
        request = ListCategoryRequest()
        
        response = use_case.execute(request)
        
        assert response is not None
        assert len(response.data) == 0
        assert isinstance(response, ListCategoryResponse)
        assert response == ListCategoryResponse(data = [])
