from dataclasses import dataclass
from uuid import UUID
from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.application.use_cases.genre_repository import GenreRepository

class DeleteGenre:
    def __init__(self, repo: GenreRepository):
        self.repo = repo
        
    @dataclass
    class Input:
        id: UUID
    
    def execute(self, input: Input) -> None:
        genre = self.repo.get_by_id(id=input.id)
        
        if genre:
            self.repo.delete(input.id)
        else:
            raise GenreNotFound(f"Genre with id {input.id} not found!")