from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Message
import json
from django.core import serializers


class WSConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_pk = self.scope['url_route']['kwargs']['pk']
        self.group_name = f'chat_{self.group_pk}'
        self.current_user = self.scope['user'].username

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'get_messages',
            }
        )

    async def get_messages(self, event):
        check = 0
        while True:
            serialized_msg, usernames = await self.get_data()
            if check >= len(serialized_msg):
                continue
            else:
                check = len(serialized_msg)
                await self.send(json.dumps({
                    'messages': serialized_msg,
                    'current_user': self.current_user,
                    'usernames': usernames,
                }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    @sync_to_async
    def get_data(self):
        messages = Message.objects.filter(group=self.group_pk).all()
        serialized_msg = serializers.serialize('json', messages)

        usernames = []
        for message in messages:
            user_id = message.user_id
            user = get_object_or_404(User, pk=user_id)
            if user:
                username = user.username
                usernames.append(username)

        return serialized_msg, usernames

