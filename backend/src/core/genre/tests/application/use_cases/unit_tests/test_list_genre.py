from unittest.mock import MagicMock

import pytest
from core.genre.application.use_cases.list_genre import ListGenre
from core.genre.domain.genre import Genre
from core.genre.application.use_cases.genre_repository import GenreRepository
from src.core._shared.listEntity import ListEntityResponse, ListPaginationInput, MetaPaginationOutput

@pytest.fixture
def action_genre() -> Genre:
    return Genre(name="Action")

@pytest.fixture
def romance_genre() -> Genre:
    return Genre(name="Romance")

@pytest.fixture
def comedy_genre() -> Genre:
    return Genre(name="Comedy")

@pytest.fixture
def genre_repo() -> GenreRepository:
    return MagicMock(GenreRepository)

class TestListGenre:
    def test_list_genre_with_categories(
        self,
        action_genre,
        romance_genre,
        genre_repo
    ):
        genre_repo.list.return_value = [romance_genre, action_genre]
        
        input = ListPaginationInput(order_by="name")
        use_case = ListGenre(genre_repo)
        output = use_case.execute(input)
        
        assert isinstance(output, ListEntityResponse)
        assert len(output.data) == 2
        assert output.data[0].name == action_genre.name
        assert output.data[1].name == romance_genre.name
        assert output.meta == MetaPaginationOutput(
            current_page=1,
            per_page=2,
            total=2
        )
        
    def test_list_genre_with_no_genres(
        self,
        genre_repo
    ):
        genre_repo.list.return_value = []
        
        input = ListPaginationInput()
        use_case = ListGenre(genre_repo)
        output = use_case.execute(input)
        
        assert isinstance(output, ListEntityResponse)
        assert len(output.data) == 0
        assert output.meta == MetaPaginationOutput(
            current_page=1,
            per_page=2,
            total=0
        )
        
    def test_list_genre_with_categories(
        self,
        action_genre,
        romance_genre,
        comedy_genre,
        genre_repo
    ):
        genre_repo.list.return_value = [comedy_genre, romance_genre, action_genre]
        
        input = ListPaginationInput(order_by="name", current_page=2)
        use_case = ListGenre(genre_repo)
        output = use_case.execute(input)
        
        assert isinstance(output, ListEntityResponse)
        assert len(output.data) == 1
        assert output.data[0].name == romance_genre.name
        assert output.meta == MetaPaginationOutput(
            current_page=2,
            per_page=2,
            total=3
        )