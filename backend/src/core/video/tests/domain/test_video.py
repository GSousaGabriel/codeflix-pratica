import uuid
import pytest
from src.core.video.domain.value_objects import AudioVideoMedia, ImageMedia
from src.core.video.domain.video import Video

class TestVideo:
    def test_create_video_successfully(self):
        video = Video("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set(), set(), set())
        
        assert video.title == "A movie"
        assert video.description == "Tense movie descripion"
        assert video.launch_year == 2000
        assert video.duration == 123.34
        assert video.published == True
        assert video.rating == "ER"
        
    def test_error_when_creating_with_empty_title(self):
        with pytest.raises(ValueError, match="Title cannot be empty."):
            Video("", "Tense movie descripion", 2000, 123.34, True, "ER", set(), set(), set())
        
    def test_error_when_creating_with_long_title(self):
        with pytest.raises(ValueError, match="Title cannot be longer than 255 characteres."):
            Video("a"*255, "Tense movie descripion", 2000, 123.34, True, "ER", set(), set(), set())
        
    def test_error_when_creating_with_no_duration(self):
        with pytest.raises(ValueError, match="Duration cannot be 0 or less."):
            Video("A movie", "Tense movie descripion", 2000, 0, True, "ER", set(), set(), set())
        
    def test_error_when_creating_with_no_duration_and_no_title(self):
        with pytest.raises(ValueError, match="Title cannot be empty.\nDuration cannot be 0 or less."):
            Video("", "Tense movie descripion", 2000, 0, True, "ER", set(), set(), set())
            
class TestUpdateVideo:
    def test_update_video_successfully(self):
        video = Video("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set(), set(), set())
        
        video.update("A serie", "Tense serie descripion", 2019, 30, False, "L")
        
        assert video.title == "A serie"
        assert video.description == "Tense serie descripion"
        assert video.launch_year == 2019
        assert video.duration == 30
        assert video.published == False
        assert video.rating == "L"
        
    def test_add_video_category(self):
        video = Video("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set(), set(), set())
        
        video.add_category(uuid.uuid4())
        
        assert len(video.categories_ids) == 1
        
    def test_add_video_genre(self):
        video = Video("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set(), set(), set())
        
        video.add_genre(uuid.uuid4())
        
        assert len(video.genres_ids) == 1
        
    def test_add_video_cast_Member(self):
        video = Video("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set(), set(), set())
        
        video.add_cast_member(uuid.uuid4())
        
        assert len(video.cast_members_ids) == 1
        
    def test_update_video_banner(self):
        video = Video("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set(), set(), set())
        
        image_media = ImageMedia(uuid.uuid4(), "Check", "Banner", "Loc")
        video.update_banner(image_media)
        
        assert video.banner is not None
        assert video.banner.name == "Banner"
        
    def test_update_video_thumbnail(self):
        video = Video("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set(), set(), set())
        
        image_media = ImageMedia(uuid.uuid4(), "Check", "Thumbnail", "Loc")
        video.update_thumbnail(image_media)
        
        assert video.thumbnail is not None
        assert video.thumbnail.name == "Thumbnail"
        
    def test_update_video_thumbnail_half(self):
        video = Video("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set(), set(), set())
        
        image_media = ImageMedia(uuid.uuid4(), "Check", "Thumbnail half", "Loc")
        video.update_thumbnail_half(image_media)
        
        assert video.thumbnail_half is not None
        assert video.thumbnail_half.name == "Thumbnail half"
        
    def test_update_video_trailer(self):
        video = Video("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set(), set(), set())
        
        image_media = ImageMedia(uuid.uuid4(), "Check", "Trailer", "Loc")
        video.update_trailer(image_media)
        
        assert video.trailer is not None
        assert video.trailer.name == "Trailer"
        
    def test_update_video(self):
        video = Video("A movie", "Tense movie descripion", 2000, 123.34, True, "ER", set(), set(), set())
        
        image_media = AudioVideoMedia(uuid.uuid4(), "Check", "Trailer", "Loc", "Raw loc", "Procesing")
        video.update_video(image_media)
        
        assert video.video is not None
        assert video.video.name == "Trailer"