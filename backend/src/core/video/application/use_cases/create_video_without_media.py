from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.notification import Notification
from src.core.castMember.application.use_cases.castMember_repository import CastMemberRepository
from src.core.category.application.use_cases.category_repository import CategoryRepository
from src.core.genre.application.use_cases.genre_repository import GenreRepository
from src.core.video.application.use_cases.exceptions import RelatedEntitiesNotFound, InvalidVideo
from src.core.video.application.use_cases.video_repository import VideoRepository
from src.core.video.domain.value_objects import Rating
from src.core.video.domain.video import Video


class CreateVideoWithoutMedia:
    @dataclass
    class Input:
        title: str
        description: str
        launch_year: int
        duration: Decimal
        published: bool
        opened: bool
        rating: Rating
        categories: set[UUID]
        genres: set[UUID]
        cast_members: set[UUID]
        
    @dataclass
    class Output:
        id: UUID
        
    def __init__(
        self,
        video_repo: VideoRepository,
        category_repo: CategoryRepository,
        genre_repo: GenreRepository,
        cast_member_repo: CastMemberRepository,
    ):
        self.video_repo = video_repo
        self.category_repo = category_repo
        self.genre_repo = genre_repo
        self.cast_member_repo = cast_member_repo
        
    def execute(self, input: Input) -> Output:
        self.validate(input)
        
        try:
            video = Video(
                title = input.title,
                description = input.description,
                launch_year = input.launch_year,
                duration = input.duration,
                published = False,
                opened = False,
                rating = input.rating,
                categories = input.categories,
                genres = input.genres,
                cast_members = input.cast_members 
            )
        except ValueError as e:
            raise InvalidVideo(e)
        
        self.video_repo.save(video)
        return self.Output(video.id)
    
    def validate(self, input: Input) -> None:
        notification = Notification()
        
        self.validate_categories(input.categories, notification)
        self.validate_genres(input.genres, notification)
        self.validate_cast_members(input.cast_members, notification)
        
        if notification.has_errors:
            raise RelatedEntitiesNotFound(notification.messages)
        
    
    def validate_categories(self, input_categories: set[UUID], notification: Notification) -> None:
        categories = [category_id.id for category_id in self.category_repo.list()]
        
        if not input_categories.issubset(categories):
            notification.add_error("Categories with provided IDs not found.")
    
    def validate_genres(self, input_genres: set[UUID], notification: Notification) -> None:
        genres = [genre_id.id for genre_id in self.genre_repo.list()]
        
        if not input_genres.issubset(genres):
            notification.add_error("Genres with provided IDs not found.")
    
    def validate_cast_members(self, input_cast_members: set[UUID], notification: Notification) -> None:
        cast_members = [cast_member.id for cast_member in self.cast_member_repo.list()]
        
        if not input_cast_members.issubset(cast_members):
            notification.add_error("Cast members with provided IDs not found.")