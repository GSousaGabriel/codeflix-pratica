from unittest.mock import create_autospec
import uuid
import pytest
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.application.use_cases.genre_repository import GenreRepository
from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.domain.genre import Genre

@pytest.fixture
def mock_genre_repo():
    return create_autospec(GenreRepository)

class TestDeleteGenre:
    def test_delete_genre_from_repository(self, mock_genre_repo):
        genre = Genre(name="Movie")
        mock_genre_repo.get_by_id.return_value = genre
        use_case = DeleteGenre(mock_genre_repo)
        use_case.execute(DeleteGenre.Input(genre.id))
        
        mock_genre_repo.delete.assert_called_once_with(genre.id)

    def test_when_genre_not_found(self, mock_genre_repo):
        mock_genre_repo.get_by_id.return_value = None
        use_case = DeleteGenre(mock_genre_repo)
        
        with pytest.raises(GenreNotFound) as exec_info:
            use_case.execute(DeleteGenre.Input(uuid.uuid4()))
        
        mock_genre_repo.delete.assert_not_called()
        assert mock_genre_repo.delete.called is False
        