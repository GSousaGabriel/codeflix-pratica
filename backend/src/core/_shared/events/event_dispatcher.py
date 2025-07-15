from abc import ABC, abstractmethod

from src.core._shared.events.event import Event

class EventDispatcher(ABC):
    @abstractmethod
    def dispatch(event: Event, video_repository)->None:
        pass