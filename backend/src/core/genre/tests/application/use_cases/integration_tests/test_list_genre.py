import pytest
from core.genre.infra.in_memory_genre_repo import InMemoryGenreRepo
from core.category.infra.in_memory_category_repo import InMemoryCategoryRepo
from core.category.domain.category import Category
from core.genre.application.use_cases.list_genre import ListGenre
from core.genre.domain.genre import Genre
from src.core._shared.listEntity import ListEntityResponse, ListPaginationInput, MetaPaginationOutput

@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")

@pytest.fixture
def serie_category() -> Category:
    return Category(name="Serie")

@pytest.fixture
def romance_genre(movie_category, serie_category) -> Genre:
    return Genre(
            name="Romance",
            categories_ids={movie_category.id, serie_category.id},
        )

@pytest.fixture
def comedy_genre(movie_category, serie_category) -> Genre:
    return Genre(
            name="Comedy",
            categories_ids={movie_category.id, serie_category.id},
        )

@pytest.fixture
def action_genre(movie_category, serie_category) -> Genre:
    return Genre(
            name="Action",
            categories_ids={movie_category.id, serie_category.id},
        )

@pytest.fixture
def category_repo(movie_category, serie_category, comedy_genre) -> InMemoryCategoryRepo:
    return InMemoryCategoryRepo([movie_category, serie_category, comedy_genre])

@pytest.fixture
def genre_repo() -> InMemoryGenreRepo:
    return InMemoryGenreRepo()

class TestListGenre:
    def test_list_genre_with_categories(
        self,
        action_genre,
        romance_genre,
        category_repo,
        genre_repo
    ):
        genre_repo.save(romance_genre)
        genre_repo.save(action_genre)
        
        input = ListPaginationInput(order_by="name")
        use_case = ListGenre(genre_repo)
        output = use_case.execute(input)
        
        assert isinstance(output, ListEntityResponse)
        assert len(output.data) == 2
        assert output.data[0].id == action_genre.id
        assert output.data[1].id == romance_genre.id
        assert output.meta == MetaPaginationOutput(
            current_page=1,
            per_page=2,
            total=2
        )
        
    def test_list_genre_with_no_genres(
        self,
        genre_repo
    ):
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
    
    def test_list_genre_with_categories_page_2(
        self,
        action_genre,
        comedy_genre,
        romance_genre,
        category_repo,
        genre_repo
    ):
        genre_repo.save(romance_genre)
        genre_repo.save(action_genre)
        genre_repo.save(comedy_genre)
        
        input = ListPaginationInput(order_by="name", current_page=2)
        use_case = ListGenre(genre_repo)
        output = use_case.execute(input)
        
        assert isinstance(output, ListEntityResponse)
        assert len(output.data) == 1
        assert output.data[0].id == romance_genre.id
        assert output.meta == MetaPaginationOutput(
            current_page=2,
            per_page=2,
            total=3
        )