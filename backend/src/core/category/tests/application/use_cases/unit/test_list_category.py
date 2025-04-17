from unittest.mock import MagicMock
from src.core._shared.listEntity import ListEntityResponse, ListPaginationInput, MetaPaginationOutput
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import CategoryOutput, ListCategory
from src.core.category.domain.category import Category

class TestListCategory:
    def test_return_all_categories_ordering_by_name(self):
        category_1 = Category(name="Serie")
        category_2 = Category(name="Movie")
        mock_repo = MagicMock(CategoryRepository)
        mock_repo.list.return_value = [category_1, category_2]
        use_case = ListCategory(mock_repo)
        request = ListPaginationInput(current_page=1, order_by="name")
        
        response = use_case.execute(request)
        
        assert response is not None
        assert len(response.data) == 2
        assert isinstance(response, ListEntityResponse)
        assert response.data[0].name == category_2.name
        assert response.data[1].name == category_1.name
        assert response.meta == MetaPaginationOutput(
                current_page=1,
                per_page=2,
                total=2
            )
        
    def test_return_all_categories_page_2(self):
        category_1 = Category(name="Serie")
        category_2 = Category(name="Movie")
        category_3 = Category(name="Cartoon")
        mock_repo = MagicMock(CategoryRepository)
        mock_repo.list.return_value = [category_1, category_2, category_3]
        use_case = ListCategory(mock_repo)
        request = ListPaginationInput(current_page=2, order_by="name")
        
        response = use_case.execute(request)
        
        assert response is not None
        assert len(response.data) == 1
        assert isinstance(response, ListEntityResponse)
        assert response.data[0].name == category_1.name
        assert response.meta == MetaPaginationOutput(
                current_page=2,
                per_page=2,
                total=3
            )
        
    def test_return_empty_list(self):
        mock_repo = MagicMock(CategoryRepository)
        mock_repo.get_by_id.return_value = []
        use_case = ListCategory(mock_repo)
        request = ListPaginationInput()
        
        response = use_case.execute(request)
        
        assert response is not None
        assert len(response.data) == 0
        assert isinstance(response, ListEntityResponse)
        assert response.data == []
        assert response.meta == MetaPaginationOutput(
                current_page=1,
                per_page=2,
                total=0
            )
