from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID

from src.core._shared.entity import Entity
from src.core.video.domain.events.event import AudioVideoMediaUpdated
from src.core.video.domain.value_objects import AudioVideoMedia, ImageMedia, MediaStatus, MediaType, Rating

@dataclass
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    opened: bool
    rating: Rating
    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]
    published: bool = field(default=False)
    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    thumbnail_trailer: ImageMedia | None = None
    video: AudioVideoMedia | None = None
    
    def __post_init__(self):
        self.validate()
        
    def update(self, title, description, launch_year, duration, published, opened, rating):
        self.title = title
        self.description = description
        self.launch_year = launch_year
        self.duration = duration
        self.published = published
        self.opened = opened
        self.rating = rating

        self.validate()
        
    def publish(self) -> None:
        if not self.video:
            self.notification.add_error("Video media is required to publish the video")
        elif self.video.status != MediaStatus.COMPLETED:
            self.notification.add_error("Video must be fully processed to be published")

        self.published = True
        self.validate()
        
    def add_category(self, category_id: UUID):
        self.categories.add(category_id)
        self.validate()
        
    def add_genre(self, genre_id: UUID):
        self.genres.add(genre_id)
        self.validate()
        
    def add_cast_member(self, cast_member: UUID):
        self.cast_members.add(cast_member)  
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
        
    def update_video_media(self, video: AudioVideoMedia) -> None:
        self.video = video
        self.validate()
        self.dispatch(AudioVideoMediaUpdated(
            aggregate_id=self.id,
            file_path=video.raw_location,
            media_type=MediaType.VIDEO
        ))
        
    def process(self, status: MediaStatus, encoded_location: str = "") -> None:
        if status == MediaStatus.COMPLETED:
            self.video = self.video.complete(encoded_location)
            self.publish()
        else:
            self.video = self.video.fail()
            
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
    
        