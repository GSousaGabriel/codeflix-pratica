from dataclasses import dataclass
from pathlib import Path
from uuid import UUID
from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.storage.abstract_storage_service import AbstractStorageService
from src.core.video.application.events.integration_events import AudioVideoMediaUpdatedIntegrationEvent
from src.core.video.application.use_cases.exceptions import InvalidVideo
from src.core.video.application.use_cases.video_repository import VideoRepository
from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType

class UploadVideo:
    @dataclass
    class Input:
        video_id: UUID
        file_name: str
        content: bytes
        content_type: str
    
    def __init__(
        self,
        video_repo: VideoRepository,
        storage_service: AbstractStorageService,
        message_bus: AbstractMessageBus
        ):
            self.video_repo = video_repo
            self.storage_service = storage_service
            self.message_bus = message_bus
       
        
    def execute(self, input: Input):
        video = self.video_repo.get_by_id(input.video_id)
        if video is None:
            raise InvalidVideo(f"Video {input.video_id} not found!")
        
        file_path = Path("videos") / str(video.id) / input.file_name
        
        self.storage_service.store(str(file_path), input.content, input.content_type)
        audio_video_media = AudioVideoMedia(
            name=input.file_name,
            raw_location=str(file_path),
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO
        )
        
        video.update_video_media(audio_video_media)
        self.video_repo.update(video)
        self.message_bus.handle([AudioVideoMediaUpdatedIntegrationEvent(
            resource_id=f"{video.id}.{MediaType.VIDEO}",
            file_path=str(file_path)
        )])