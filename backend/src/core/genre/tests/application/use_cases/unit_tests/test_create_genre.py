from unittest.mock import create_autospec
import uuid
import pytest
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.domain.category import Category
from src.core.genre.application.use_cases.create_genre import CreateGenre
from src.core.genre.application.use_cases.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")

@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository

class TestCreateGenre:
    def test_create_genre_without_existing_category(
        self,
        mock_empty_category_repository,
        mock_genre_repository
    ):
        use_case = CreateGenre(mock_genre_repository, mock_empty_category_repository)
        category_id=uuid.uuid4()
        input = CreateGenre.Input(name="Drama", categories_ids={category_id})
        
        with pytest.raises(RelatedCategoriesNotFound) as exec_info:
            use_case.execute(input)
        
        assert str(category_id) in str((exec_info.value))
        
    def test_when_genre_is_invalid(
        self,
        movie_category,
        mock_category_repository_with_categories,
        mock_genre_repository
    ):
        use_case = CreateGenre(mock_genre_repository, mock_category_repository_with_categories)
        input = CreateGenre.Input(name="", categories_ids={movie_category.id})
        
        with pytest.raises(InvalidGenre):
            use_case.execute(input)
            
    def test_created_genre_with_valid_data(
        self,
        movie_category,
        documentary_category,
        mock_category_repository_with_categories,
        mock_genre_repository
    ):
        use_case = CreateGenre(mock_genre_repository, mock_category_repository_with_categories)
        input = CreateGenre.Input(name="Drama", categories_ids={movie_category.id, documentary_category.id})
        output = use_case.execute(input)
        
        assert isinstance(output.id, uuid.UUID)
        mock_genre_repository.save.assert_called_once_with(
            Genre(
                id=output.id,
                name="Drama",
                is_active=True,
                categories_ids={movie_category.id, documentary_category.id}
            )
        )
            
    def test_created_genre_without_category(
        self,
        mock_category_repository_with_categories,
        mock_genre_repository
    ):
        use_case = CreateGenre(mock_genre_repository, mock_category_repository_with_categories)
        input = CreateGenre.Input(name="Drama")
        output = use_case.execute(input)
        
        assert isinstance(output.id, uuid.UUID)
        mock_genre_repository.save.assert_called_once_with(
            Genre(
                id=output.id,
                name="Drama",
                is_active=True
            )
        )