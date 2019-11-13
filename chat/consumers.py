import json
import datetime

from django.conf import settings

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, message):
        print("connecte", message)

    async def websocket_receive(self, message):
        print("recevie", message)

    async def websocket_disconnect(self, message):
        print("disconnected", message)