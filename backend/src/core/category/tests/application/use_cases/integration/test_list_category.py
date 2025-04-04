from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.application.use_cases.list_category import CategoryOutput, ListCategory, ListCategoryResponse, ListCategoryRequest
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repo import InMemoryCategoryRepo

class TestListCategory:
    def test_return_all_categories(self):
        category_movie = Category(name="Movie", description="Movie category")
        category_serie = Category(name="Serie", description="Serie category")
        repo = InMemoryCategoryRepo(categories=[category_movie, category_serie])
        use_case = ListCategory(repo)
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
        repo = InMemoryCategoryRepo()
        use_case = ListCategory(repo)
        request = ListCategoryRequest()
        
        response = use_case.execute(request)
        
        assert response is not None
        assert len(response.data) == 0
        assert isinstance(response, ListCategoryResponse)
        assert response == ListCategoryResponse(data = [])
