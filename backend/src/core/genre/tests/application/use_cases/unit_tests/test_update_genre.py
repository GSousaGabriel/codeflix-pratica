from unittest.mock import create_autospec
import uuid
import pytest
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.category.domain.category import Category
from src.core.genre.application.use_cases.genre_repository import GenreRepository
from src.core.genre.application.use_cases.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre

@pytest.fixture
def mock_genre_repo() -> GenreRepository:
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

class TestUpdateGenre:
    def test_update_genre_from_repository(
        self,
        movie_category,
        mock_genre_repo,
        mock_category_repository_with_categories
    ):
        genre = Genre(name="Movie")
        mock_genre_repo.get_by_id.return_value = genre
        use_case = UpdateGenre(mock_genre_repo, mock_category_repository_with_categories)
        use_case.execute(UpdateGenre.Input(genre.id, name="Drama", is_active=False, categories_ids={movie_category.id}))
        
        mock_genre_repo.update.assert_called_once_with(genre)
        assert genre.name == "Drama"
        assert genre.is_active is False
        assert movie_category.id in genre.categories_ids
        assert len(genre.categories_ids) == 1
        
    def test_update_genre_with_multiples_categories_from_repository(
        self,
        movie_category,
        documentary_category,
        mock_genre_repo,
        mock_category_repository_with_categories
    ):
        genre = Genre(name="Movie", categories_ids={uuid.uuid4()})
        mock_genre_repo.get_by_id.return_value = genre
        use_case = UpdateGenre(mock_genre_repo, mock_category_repository_with_categories)
        use_case.execute(UpdateGenre.Input(genre.id, categories_ids={movie_category.id, documentary_category.id}))
        
        mock_genre_repo.update.assert_called_once_with(genre)
        assert genre.name == "Movie"
        assert genre.is_active is True
        assert movie_category.id in genre.categories_ids
        assert documentary_category.id in genre.categories_ids
        assert len(genre.categories_ids) == 2

    def test_when_genre_not_found(
        self,
        mock_genre_repo,
        mock_category_repository_with_categories
    ):
        mock_genre_repo.get_by_id.return_value = None
        use_case = UpdateGenre(mock_genre_repo, mock_category_repository_with_categories)
        
        with pytest.raises(GenreNotFound, match="Genre with id .* was not found!") as exec_info:
            use_case.execute(UpdateGenre.Input(uuid.uuid4()))
        
        mock_genre_repo.update.assert_not_called()
        assert mock_genre_repo.update.called is False

    def test_when_genre_name_update_is_invalid(
        self,
        mock_genre_repo,
        mock_category_repository_with_categories
    ):
        genre = Genre(name="Movie")
        mock_genre_repo.get_by_id.return_value = genre
        use_case = UpdateGenre(mock_genre_repo, mock_category_repository_with_categories)
        
        with pytest.raises(InvalidGenre) as exec_info:
            use_case.execute(UpdateGenre.Input(genre.id, name=""))
        
        mock_genre_repo.update.assert_not_called()
        assert mock_genre_repo.update.called is False

    def test_when_genre_category_update_is_invalid(
        self,
        mock_genre_repo,
        mock_category_repository_with_categories
    ):
        genre = Genre(name="Movie")
        mock_genre_repo.get_by_id.return_value = genre
        use_case = UpdateGenre(mock_genre_repo, mock_category_repository_with_categories)
        
        with pytest.raises(RelatedCategoriesNotFound, match="Some of the categories could no be found!") as exec_info:
            use_case.execute(UpdateGenre.Input(genre.id, categories_ids={uuid.uuid4()}))
        
        mock_genre_repo.update.assert_not_called()
        assert mock_genre_repo.update.called is False
        