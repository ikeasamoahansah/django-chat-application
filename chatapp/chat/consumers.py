import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message

class ChatConsumer(WebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']

        await self.channel_layer.group_add(
            self.room_id,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self):
        await self.channel_layer.group_discard(
            f"chat_{self.room_id}",
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = self.scope["user"].id

        await self.save_message(sender_id, message)

        await self.channel_layer.group_send(
            f"chat_{self.room_id}",
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope["user"].username
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'sender': sender
        }))

    async def save_message(self, sender_id, message):
        await Message.objects.create(sender=sender_id, id=self.room_id, content=message)