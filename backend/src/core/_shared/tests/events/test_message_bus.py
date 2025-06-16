
from unittest.mock import create_autospec
from src.core._shared.application.handler import Handler
from src.core._shared.events.message_bus import MessageBus

class DummyEvent:
    pass

class TestMessageBus:
    def test_class_correct_handler_with_event(self):
        message_bus= MessageBus()
        dummy_handler = create_autospec(Handler)
        message_bus.handlers[DummyEvent] = [dummy_handler]
        event = DummyEvent()
        message_bus.handle([event])
        
        dummy_handler.handle.assert_called_once_with(event)