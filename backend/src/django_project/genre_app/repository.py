from uuid import UUID
from django.db import transaction
from src.core.genre.application.use_cases.genre_repository import GenreRepository
from django_project.genre_app.models import Genre as GenreModel
from src.core.genre.domain.genre import Genre

class DjangoORMGenreRepository(GenreRepository):
    def __init__(self, genre_model: GenreModel = GenreModel):
        self.genre_model = genre_model
        
    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            new_genre = self.genre_model.objects.create(
                id = genre.id,
                name = genre.name,
                is_active = genre.is_active
            )
            new_genre.categories_ids.set(genre.categories_ids)
        

    def update(self, genre: Genre) -> None:
        try:
            genre_instance = self.genre_model.objects.get(pk=genre.id)
        except self.genre_model.DoesNotExist:
            return None
        
        with transaction.atomic():
            self.genre_model.objects.filter(pk=genre.id).update(
                name=genre.name,
                is_active=genre.is_active,
            )
            genre_instance.categories_ids.set(genre.categories_ids)
        
    def get_by_id(self, id: UUID)-> Genre | None:
        try:
            genre = self.genre_model.objects.get(pk=id)
            return Genre(
                id = genre.id,
                name = genre.name,
                categories_ids = set(genre.categories_ids.values_list("id", flat=True)),
                is_active = genre.is_active
            )
        except self.genre_model.DoesNotExist:
            return None
        
    def delete(self, id: UUID):
        self.genre_model.objects.filter(pk=id).delete()
        
    def list(self)-> list[Genre]:
        return [Genre(
                id = genre.id,
                name = genre.name,
                categories_ids = set(genre.categories_ids.values_list("id", flat=True)),
                is_active = genre.is_active
            ) for genre in self.genre_model.objects.all()]