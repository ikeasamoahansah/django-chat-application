import json
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Room

class ChatConsumer(WebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.accept()

        await self.get_room()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        self.message.reply_channel.send({"accept": True})

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = self.scope["user"].id

        await self.save_message(sender_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope["user"].username
            }
        )
    
    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'sender': event['sender']
        }))

    async def get_room(self):
        self.room = Room.objects.get(id=self.room_name)

    async def save_message(self, sender_id, message):
        message = Message.objects.create(sender=sender_id, content=message)

        await self.room.messages.add(message)