from unittest.mock import MagicMock
from core.category.domain.category import Category
from core.genre.application.use_cases.list_genre import ListGenre
from core.genre.domain.genre import Genre
from core.genre.application.use_cases.genre_repository import GenreRepository

class TestListGenre:
    def test_list_genre_with_categories(self):
        movie_category = Category(name="Movie")
        serie_category = Category(name="Serie")
        genre = Genre(
            name="Action",
            categories_ids={movie_category.id, serie_category.id},
        )
        
        mock_genre_repo = MagicMock(GenreRepository)
        mock_genre_repo.list.return_value = [genre]
        
        use_case = ListGenre(mock_genre_repo)
        output = use_case.execute()
        
        assert len(output.data) == 1
        assert output.data[0].id == genre.id
        
    def test_list_genre_with_no_genres(self):
        mock_genre_repo = MagicMock(GenreRepository)
        mock_genre_repo.list.return_value = []
        
        use_case = ListGenre(mock_genre_repo)
        output = use_case.execute()
        
        assert len(output.data) == 0