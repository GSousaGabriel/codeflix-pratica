from src.core._shared.listEntity import ListEntityResponse, ListPaginationInput, MetaPaginationOutput
from src.core.category.application.use_cases.list_category import ListCategory
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repo import InMemoryCategoryRepo

class TestListCategory:
    def test_return_all_categories(self):
        category_movie = Category(name="Movie", description="Movie category")
        category_serie = Category(name="Serie", description="Serie category")
        repo = InMemoryCategoryRepo(categories=[category_movie, category_serie])
        use_case = ListCategory(repo)
        request = ListPaginationInput(order_by="name")
        
        response = use_case.execute(request)
        
        assert response is not None
        assert len(response.data) == 2
        assert isinstance(response, ListEntityResponse)
        assert response.data[0].name == category_movie.name
        assert response.data[1].name == category_serie.name
        assert response.meta == MetaPaginationOutput(
            current_page=1,
            per_page=2,
            total=2
        )
        
    def test_return_all_categories_page_2(self):
        category_movie = Category(name="Movie", description="Movie category")
        category_serie = Category(name="Serie", description="Serie category")
        category_cartoon = Category(name="Cartoon", description="Cartoon category")
        repo = InMemoryCategoryRepo(categories=[category_movie, category_serie, category_cartoon])
        use_case = ListCategory(repo)
        request = ListPaginationInput(current_page=2, order_by="name")
        
        response = use_case.execute(request)
        
        assert response is not None
        assert len(response.data) == 1
        assert isinstance(response, ListEntityResponse)
        assert response.data[0].name == category_serie.name
        assert response.meta == MetaPaginationOutput(
            current_page=2,
            per_page=2,
            total=3
        )
        
    def test_return_empty_list(self):
        repo = InMemoryCategoryRepo()
        use_case = ListCategory(repo)
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
