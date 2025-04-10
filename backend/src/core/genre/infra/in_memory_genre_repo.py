from uuid import UUID

from src.core.genre.domain.genre import Genre


class InMemoryGenreRepo:
    def __init__(self, categories=None):
        self.categories = categories or []
        
    def save(self, genre):
        self.categories.append(genre)
        
    def get_by_id(self, id: UUID) -> Genre | None:
        return next((genre for genre in self.categories if genre.id == id), None)
        
    def delete(self, id: UUID) -> None:
        genre = self.get_by_id(id)
        self.categories.remove(genre)
        
    def update(self, genre: Genre) -> None:
        od_genre = self.get_by_id(genre.id)
        
        if genre:
            self.categories.remove(od_genre)
            self.categories.append(genre)
        
    def list(self) -> list[Genre]:
        return [genre for genre in self.categories]