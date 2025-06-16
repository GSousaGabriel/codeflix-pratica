from unittest.mock import create_autospec

import pytest
from src.core._shared.events.message_bus import MessageBus
from src.core._shared.storage.abstract_storage_service import AbstractStorageService
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core.video.application.use_cases.exceptions import InvalidVideo
from src.core.video.application.use_cases.upload_video import UploadVideo
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType
from src.core.video.domain.video import Video
from src.core.video.infra.in_memory_video_repo import InMemoryVideoRepository

class TestUploadVideo:
    def test_upload_video_media_to_video(self):
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
        video_repo = InMemoryVideoRepository(videos=[video])
        mock_storage = create_autospec(AbstractStorageService)
        mock_message_bus = create_autospec(MessageBus)
        
        input = UploadVideo.Input(
                video_id=video.id,
                file_name="video.mp4",
                content=b"video content",
                content_type="video/mp4"
            )
        use_case = UploadVideo(video_repo, mock_storage, mock_message_bus)
        use_case.execute(input)
        
        vide_from_repo = video_repo.get_by_id(video.id)
        
        assert vide_from_repo is not None
        mock_storage.store.assert_called_once_with(
            f"videos/{video.id}/video.mp4",
            b"video content",
            "video/mp4"
        )
        assert vide_from_repo.video == AudioVideoMedia(
            name="video.mp4",
            raw_location=f"videos/{video.id}/video.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO
        )
        mock_message_bus.handle.assert_called_once_with([
            AudioVideoMediaUpdatedIntegrationEvent(
                resource_id=f"{video.id}.{MediaType.VIDEO}",
                file_path=f"videos/{video.id}/video.mp4"
            )
        ])
        
    def test_upload_video_media_when_video_does_not_exist(self):
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
        video_repo = InMemoryVideoRepository()
        mock_storage = create_autospec(AbstractStorageService)
        mock_message_bus = create_autospec(MessageBus)
        
        input = UploadVideo.Input(
                video_id=video.id,
                file_name="video.mp4",
                content=b"video content",
                content_type="video/mp4"
            )
        use_case = UploadVideo(video_repo, mock_storage, mock_message_bus)
        
        with pytest.raises(InvalidVideo, match="Video .* not found!"):
            use_case.execute(input)