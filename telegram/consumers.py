from channels.generic.websocket import WebsocketConsumer
import json


class WSConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        # code
        self.send(json.dumps({'message': None}))
