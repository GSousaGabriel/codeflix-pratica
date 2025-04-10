from dataclasses import dataclass, field
from uuid import UUID
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.genre.application.use_cases.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.genre_repository import GenreRepository
from src.core.genre.domain.genre import Genre


class CreateGenre:
    def __init__(self, repo: GenreRepository, category_repo: CategoryRepository):
        self.repo = repo
        self.category_repo = category_repo
        
    @dataclass
    class Input:
        name: str
        categories_ids: set[UUID] = field(default_factory=set)
        is_active: bool = True
        
    @dataclass
    class Output:
        id: UUID
    
    def execute(self, input: Input) -> Output:
        categories_ids = {category.id for category in self.category_repo.list()}
        
        if not input.categories_ids.issubset(categories_ids):
            raise RelatedCategoriesNotFound(f"Categories not found {input.categories_ids - categories_ids}")
        
        try:
            genre = Genre(name=input.name, is_active=input.is_active, categories_ids=input.categories_ids)
        except ValueError as e:
            raise InvalidGenre(str(e))
        
        self.repo.save(genre)
        return self.Output(genre.id)