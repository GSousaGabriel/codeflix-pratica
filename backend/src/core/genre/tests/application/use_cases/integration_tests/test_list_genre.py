from core.genre.infra.in_memory_genre_repo import InMemoryGenreRepo
from core.category.infra.in_memory_category_repo import InMemoryCategoryRepo
from core.category.domain.category import Category
from core.genre.application.use_cases.list_genre import ListGenre
from core.genre.domain.genre import Genre

class TestListGenre:
    def test_list_genre_with_categories(self):
        category_repo = InMemoryCategoryRepo()
        movie_category = Category(name="Movie")
        serie_category = Category(name="Serie")
        
        category_repo.save(movie_category)
        category_repo.save(serie_category)
        genre_repo = InMemoryGenreRepo()
        
        genre = Genre(
            name="Action",
            categories_ids={movie_category.id, serie_category.id},
        )
        genre_repo.save(genre)
        
        use_case = ListGenre(genre_repo)
        output = use_case.execute()
        
        assert len(output.data) == 1
        assert output.data[0].id == genre.id
        
    def test_list_genre_with_no_genres(self):
        genre_repo = InMemoryGenreRepo()
        
        use_case = ListGenre(genre_repo)
        output = use_case.execute()
        
        assert len(output.data) == 0