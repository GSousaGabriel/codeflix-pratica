from abc import ABC, abstractmethod

from src.core._shared.events.event import Event

class EventDispatcher(ABC):
    @abstractmethod
    def dispatch(event: Event)->None:
        pass