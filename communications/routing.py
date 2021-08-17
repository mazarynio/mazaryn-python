from django.urls import re_path

from .consumers import ChatConsumer

"""Routing to work out what single consumer to give a connection to """
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<friend>\w+)/$', ChatConsumer.as_asgi()),
]
