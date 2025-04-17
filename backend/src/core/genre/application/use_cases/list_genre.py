from dataclasses import dataclass
from uuid import UUID
from src.core._shared.listEntity import ListEntity, ListEntityResponse, ListPaginationInput
from src.core.genre.application.use_cases.genre_repository import GenreRepository

@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories_ids: set[UUID]

class ListGenre(ListEntity):
    def __init__(self, repo=GenreRepository):
        self.repo = repo    
    
    def execute(self, input: ListPaginationInput)-> ListEntityResponse[GenreOutput]:
        genres = self.repo.list()
        sorted_genre = sorted(
            [
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories_ids={category for category in genre.categories_ids}
                )
                for genre in genres
            ], key= lambda genre: getattr(genre, input.order_by)
        )
        
        return self.paginate_data(input.current_page, sorted_genre)