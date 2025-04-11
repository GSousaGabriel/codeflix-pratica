from dataclasses import dataclass, field
from uuid import UUID
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.genre.application.use_cases.genre_repository import GenreRepository
from src.core.genre.application.use_cases.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound

class UpdateGenre:
    def __init__(self, repo: GenreRepository, category_repo: CategoryRepository):
        self.repo = repo
        self.category_repo = category_repo
        
    @dataclass
    class Input:
        id: UUID
        name: str | None = None
        categories_ids: set[UUID] = field(default_factory=set)
        is_active: bool | None = None
        
    def execute(self, input: Input):
        genre = self.repo.get_by_id(input.id)
        
        if genre is None:
            raise GenreNotFound(f"Genre with id {input.id} was not found!")
        
        try:
            genre.clear_category()
            
            if input.is_active is True:
                genre.activate()

            if input.is_active is False:
                genre.deactivate()
                
            if input.name is not None:
                genre.change_name(input.name)

            if input.categories_ids:
                valid_categories_id = [category_id.id for category_id in self.category_repo.list()]
                
                if not input.categories_ids.issubset(valid_categories_id):
                    raise RelatedCategoriesNotFound("Some of the categories could no be found!")
                    
                for category_id in input.categories_ids:
                    genre.add_category(category_id)

        except ValueError as error:
            raise InvalidGenre(error)
            
        self.repo.update(genre)