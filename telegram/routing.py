from django.urls import re_path, path
from .consumers import WSConsumer

ws_urlpatterns = [
    path('ws/get_messages/<int:pk>', WSConsumer.as_asgi())
]
