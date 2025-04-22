from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from src.core._shared.entity import Entity
from src.core.video.domain.value_objects import AudioVideoMedia, ImageMedia, Rating

@dataclass
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    published: bool
    rating: Rating
    categories_ids: set[UUID]
    genres_ids: set[UUID]
    cast_members_ids: set[UUID]
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    thumbnail_trailer: ImageMedia | None = None
    video: AudioVideoMedia | None = None
    
    def __post_init__(self):
        self.validate()
        
    def update(self, title, description, launch_year, duration, published, rating):
        self.title = title
        self.description = description
        self.launch_year = launch_year
        self.duration = duration
        self.published = published
        self.rating = rating

        self.validate()
        
    def add_category(self, category_id: UUID):
        self.categories_ids.add(category_id)
        self.validate()
        
    def add_genre(self, genre_id: UUID):
        self.genres_ids.add(genre_id)
        self.validate()
        
    def add_cast_member(self, cast_member: UUID):
        self.cast_members_ids.add(cast_member)  
        self.validate()
        
    def update_banner(self, banner: ImageMedia):
        self.banner = banner
        self.validate()
        
    def update_thumbnail(self, thumbnail: ImageMedia) -> None:
        self.thumbnail = thumbnail
        self.validate()
        
    def update_thumbnail_half(self, thumbnail_half: ImageMedia) -> None:
        self.thumbnail_half = thumbnail_half
        self.validate()
        
    def update_trailer(self, trailer: ImageMedia):
        self.trailer = trailer
        self.validate()
        
    def update_video(self, video: AudioVideoMedia) -> None:
        self.video = video
        self.validate()
            
    def validate(self):
        if not self.title:
            self.notification.add_error("Title cannot be empty.")
            
        if len(self.title) > 254:
            self.notification.add_error("Title cannot be longer than 255 characteres.")
        
        if self.duration <= 0:
            self.notification.add_error("Duration cannot be 0 or less.")
            
        if self.notification.has_errors:
            raise ValueError(self.notification.messages)
    
        