
import pytest

from django_project.genre_app.repository import DjangoORMGenreRepository
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.mark.django_db
class TestSave:
    def test_saves_genre_in_database(self):
        genre = Genre(name="Action")
        genre_repo = DjangoORMGenreRepository()
        genre_repo.save(genre)
        
        assert genre_repo.genre_model.objects.count() == 1
        assert genre_repo.genre_model.objects.first().id == genre.id
        assert genre_repo.genre_model.objects.first().name == "Action"
        
    def test_saves_genre_in_database_with_categories(self):
        genre = Genre(name="Action")
        category = Category(name="Adventure")
        genre_repo = DjangoORMGenreRepository()
        category_repo = DjangoORMCategoryRepository()
        category_repo.save(category)
        
        genre.add_category(category.id)
        genre_repo.save(genre)
        related_category = genre_repo.genre_model.objects.first().categories_ids.first()
        
        assert genre_repo.genre_model.objects.first().categories_ids.count() == 1
        assert related_category.id == category.id
        assert related_category.name == "Adventure"