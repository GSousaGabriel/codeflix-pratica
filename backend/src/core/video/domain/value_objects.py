from dataclasses import dataclass
from enum import Enum, auto
from uuid import UUID

class MediaStatus(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    ERROR = auto()
    
class Rating(Enum):
    ER = auto()
    L = auto()
    age_10 = auto()
    age_12 = auto()
    age_14 = auto()
    age_16 = auto()
    age_18 = auto()

@dataclass(frozen=True)
class ImageMedia:
    id: UUID
    check_sum: str
    name: str
    location: str
    
@dataclass(frozen=True)
class AudioVideoMedia:
    id: UUID
    check_sum: str
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus