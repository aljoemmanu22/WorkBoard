from channels.generic.websocket import WebsocketConsumer
import json

class TaskBoardConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        # Broadcast the data to all connected clients
        self.send(text_data=json.dumps(data))
