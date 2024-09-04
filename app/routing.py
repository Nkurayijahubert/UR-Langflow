from django.urls import path

# Import consumers lazily
def get_consumers():
    from . import consumers
    return consumers

websocket_urlpatterns = [
    path('ws/chat/', get_consumers().LangflowConsumer.as_asgi()),
]