from channels.generic.websocket import AsyncWebsocketConsumer
import json

class OpenSauceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.lobby_name = self.scope['url_route']['kwargs']['lobby_name']
        self.lobby_group_name = 'lobby_%s' % self.lobby_name

        # Join lobby group
        await self.channel_layer.group_add(
            self.lobby_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'message': 'test'
        }))

    async def disconnect(self, close_code):
        # Leave lobby group
        await self.channel_layer.group_discard(
            self.lobby_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to lobby group
        await self.channel_layer.group_send(
            self.lobby_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from lobby group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
