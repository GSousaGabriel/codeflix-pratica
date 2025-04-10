from dataclasses import dataclass
from uuid import UUID
from src.core.genre.application.use_cases.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre

@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: set[UUID]

class ListGenre:
    def __init__(self, repo=GenreRepository):
        self.repo = repo
        
    @dataclass
    class Input:
        pass
    
    @dataclass
    class Output:
        data: list[GenreOutput]      
    
    def execute(self)-> Output:
        genres = self.repo.list()
        
        return self.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories={category for category in genre.categories_ids}
                )
                for genre in genres
            ]
        )