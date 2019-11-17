from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack

import content.routing

application = ProtocolTypeRouter({
    #만약에 websocket protocol 이라면, AuthMiddlewareStack
    # URLRouter 로 연결, 소비자의 라우트 연결 HTTP path를 조사
    'websocket': AuthMiddlewareStack(
        URLRouter(

            content.routing.websocket_urlpatterns
        )
    ),
})