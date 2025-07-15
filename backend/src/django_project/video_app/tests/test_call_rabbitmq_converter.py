import json
import pika
from src.core._shared.events.event_dispatcher import EventDispatcher

class RabbitMQDispatcherTest(EventDispatcher):
    def __init__(self, host="localhost", queue="videos.converted"):
        self.host=host
        self.queue = queue
        self.connection=None
        self.channel=None
    
    def dispatch(self, id: str) -> None:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
            ),
        )
        channel = connection.channel()
        channel.queue_declare(queue= self.queue)

        message = {
            "error": "",
            "video": {
                "resource_id": f"{id}.VIDEO",
                "encoded_video_folder": "/path/to/encoded/video",
            },
            "status": "COMPLETED",
        }
        channel.basic_publish(exchange='', routing_key= self.queue, body=json.dumps(message))

        print("Sent message")
        
    def close(self):
        self.connection.close()