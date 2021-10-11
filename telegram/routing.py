from django.urls import path
from .consumers import WSConsumer

ws_urlpatterns = [
    path('ws/get_messages/<int:pk>', WSConsumer.as_asgi())
]
