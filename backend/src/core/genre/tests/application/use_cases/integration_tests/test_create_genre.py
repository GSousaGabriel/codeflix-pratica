import uuid
import pytest
from core.category.application.use_cases.category_repository import CategoryRepository
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repo import InMemoryCategoryRepo
from core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.exceptions import InvalidGenre, RelatedCategoriesNotFound
from core.genre.infra.in_memory_genre_repo import InMemoryGenreRepo

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def category_repo(movie_category, documentary_category)-> CategoryRepository:
    return InMemoryCategoryRepo(
        categories=[movie_category, documentary_category]
    )

class TestCreateGenre:
    def test_create_genre_with_categories(
        self,
        movie_category,
        documentary_category,
        category_repo,
    ):
        genre_repo = InMemoryGenreRepo()
        use_case = CreateGenre(genre_repo, category_repo)
        input = CreateGenre.Input(name="Drama", categories_ids={movie_category.id, documentary_category.id})
        
        output = use_case.execute(input)
        saved_genre = genre_repo.get_by_id(output.id)
        
        assert isinstance(output.id, uuid.UUID)
        assert  saved_genre is not None
        assert  saved_genre.categories_ids == {movie_category.id, documentary_category.id}
        
    
    def test_create_genre_without_existing_category(
        self,
        category_repo
    ):
        genre_repo = InMemoryGenreRepo()
        use_case = CreateGenre(genre_repo, category_repo)
        category_id=uuid.uuid4()
        input = CreateGenre.Input(name="Drama", categories_ids={category_id})
        
        with pytest.raises(RelatedCategoriesNotFound) as exec_info:
            use_case.execute(input)
        
        assert str(category_id) in str((exec_info.value))
        assert genre_repo.list() == []
        
    def test_when_genre_is_invalid(
        self,
        movie_category,
        category_repo
    ):
        genre_repo = InMemoryGenreRepo()
        use_case = CreateGenre(genre_repo, category_repo)
        input = CreateGenre.Input(name="", categories_ids={movie_category.id})
        
        with pytest.raises(InvalidGenre):
            use_case.execute(input)
            
        assert genre_repo.list() == []