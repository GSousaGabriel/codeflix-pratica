from dataclasses import dataclass
from src.core._shared.events.event import Event

@dataclass(frozen=True)
class VideoToConvert:
    resource_id: str
    encoded_video_folder: str

@dataclass(frozen=True)
class AudioVideoMediaUpdatedIntegrationEvent(Event):
    resource_id: str
    file_path: str