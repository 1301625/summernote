from django.conf import settings

from .models import Chatroom,Post

import json
import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # content/routing.py 정의된 URL 파라미터에서 pk 얻기
        self.room_name = self.scope['url_route']['kwargs']['pk'] #해당 게시글 번호
        self.room_group_name = '%s_chat' % self.room_name

        self.room_object = await self.get_Post()   #title 제목
        author = self.room_object.author
        user_post_include =  await self.user_Check()

        print(self.scope['user'].id)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        #비로그인 , 작성자가 아닌경우 , 해당 게시글에 신청자가 아닌경우 소켓에 접근할수 없음
        if self.scope["user"].is_anonymous or author != self.scope['user'] and not user_post_include:
            await self.close()
        else:
            await self.accept()  # 웹 소켓 연결 허용

    # 연결 해제
    async def disconnect(self, code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    #웹소켓에서 메세지를 받아 처리하는 부분
    async def receive(self, text_data):

        text_data_json = json.loads(text_data)  # room.html chatSocket.send에서 받은 데이터
        print(text_data_json)
        message = text_data_json['message_json']

        #message 공백인 경우 , str 문자열이 아닌경우
        if len(message) <= 0 or type(message) != str:
            return

        user = self.scope['user'] #왜 문제인지 모르겠음, 현재 접속한 유저
        user_name= user.nickname if user.nickname else user.name # 닉네임이 존재한다면 닉네임 없다면 이름

        await self.create_chat_message(message,user,self.room_name)

        user = str(user)  #str으로 바꾸지않으면 웹소켓에 보낼때 오류

        pk = self.room_name

        now_time = datetime.datetime.now().strftime(settings.DATETIME_FORMAT)


        #그룹에 보낼 데이터
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # 이벤트는 특별이 'type'이벤트를받을 소비자 호출하는 메소드의 이름에 해당하는 키를 누릅니다
                'message': message,
                'user' : user,
                'now_time': now_time,
                'user_name': user_name,
            }
        )

    #위의 receive 메서드에서 그룹으로 메세지를 보내면 그 메세지를 받아 처리하는 부분
    async def chat_message(self, event):
        message = event['message']
        now_time = event['now_time']
        user = event['user']
        user_name = event['user_name']


        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
            'now_time': now_time,
            'user_name': user_name,
        }))



    @database_sync_to_async
    def create_chat_message(self, message, user, pk):
        Chatroom.objects.create(post_id=pk, user=user,message=message)

    @database_sync_to_async
    def get_Post(self):
        return Post.objects.get(pk=self.room_name)

    #TODO 필요한 데이터만 뽑아내기(user만 post제외)
    #스터디 신청자만 웹소켓 입장
    @database_sync_to_async
    def user_Check(self):
        return Post.objects.get(pk=self.room_name).apply_set.filter(user=self.scope['user']).only('user')

