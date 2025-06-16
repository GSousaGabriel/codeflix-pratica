import uuid
import pytest
from src.core.video.domain.events.event import AudioVideoMediaUpdated
from src.core.video.domain.value_objects import AudioVideoMedia, ImageMedia, MediaStatus, MediaType
from src.core.video.domain.video import Video

class TestVideo:
    def test_create_video_successfully(self):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
        assert video.title == "A movie"
        assert video.description == "Tense movie descripion"
        assert video.launch_year == 2000
        assert video.duration == 123.34
        assert video.published == False
        assert video.opened == False
        assert video.rating == "ER"
        
    def test_error_when_creating_with_empty_title(self):
        with pytest.raises(ValueError, match="Title cannot be empty."):
            Video(
            title = "", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
    def test_error_when_creating_with_long_title(self):
        with pytest.raises(ValueError, match="Title cannot be longer than 255 characteres."):
            Video(
            title = "a"*255, 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
    def test_error_when_creating_with_no_duration(self):
        with pytest.raises(ValueError, match="Duration cannot be 0 or less."):
            Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=0,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
    def test_error_when_creating_with_no_duration_and_no_title(self):
        with pytest.raises(ValueError, match="Title cannot be empty.\nDuration cannot be 0 or less."):
            Video(
            title = "", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=0,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
            
class TestUpdateVideo:
    def test_update_video_successfully(self):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
        video.update("A serie", "Tense serie descripion", 2019, 30, False, True, "L")
        
        assert video.title == "A serie"
        assert video.description == "Tense serie descripion"
        assert video.launch_year == 2019
        assert video.duration == 30
        assert video.published == False
        assert video.opened == True
        assert video.rating == "L"
        
    def test_add_video_category(self):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
        video.add_category(uuid.uuid4())
        
        assert len(video.categories) == 1
        
    def test_add_video_genre(self):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
        video.add_genre(uuid.uuid4())
        
        assert len(video.genres) == 1
        
    def test_add_video_cast_Member(self):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
        video.add_cast_member(uuid.uuid4())
        
        assert len(video.cast_members) == 1
        
    def test_update_video_banner(self):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
        image_media = ImageMedia("Banner", "Loc")
        video.update_banner(image_media)
        
        assert video.banner is not None
        assert video.banner.name == "Banner"
        
    def test_update_video_thumbnail(self):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
        image_media = ImageMedia("Thumbnail", "Loc")
        video.update_thumbnail(image_media)
        
        assert video.thumbnail is not None
        assert video.thumbnail.name == "Thumbnail"
        
    def test_update_video_thumbnail_half(self):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
        image_media = ImageMedia("Thumbnail half", "Loc")
        video.update_thumbnail_half(image_media)
        
        assert video.thumbnail_half is not None
        assert video.thumbnail_half.name == "Thumbnail half"
        
    def test_update_video_trailer(self):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
        image_media = ImageMedia("Trailer", "Loc")
        video.update_trailer(image_media)
        
        assert video.trailer is not None
        assert video.trailer.name == "Trailer"
        
    def test_update_video(self):
        video = Video(
            title = "A movie", 
            description="Tense movie descripion",
            launch_year=2000, 
            duration=123.34,
            published=False,
            opened= False,
            rating="ER",
            genres=set(),
            cast_members=set(),
            categories=set()
        )
        
        video_media = AudioVideoMedia("Trailer", "Loc", "Raw loc", MediaStatus.COMPLETED, MediaType.VIDEO)
        video.update_video_media(video_media)
        
        assert video.video is not None
        assert video.video == video_media
        assert video.events == [AudioVideoMediaUpdated(
            aggregate_id=video.id,
            file_path=video_media.raw_location,
            media_type=MediaType.VIDEO
        )]
        assert video.video.name == "Trailer"