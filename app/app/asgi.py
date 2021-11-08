import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django_asgi_app = get_asgi_application()

from app.middleware import JWTAuthMiddlewareStack
from django.urls import re_path
from .consumers import EchoConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$', EchoConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
  "http": django_asgi_app,
  "websocket": JWTAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
