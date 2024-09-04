import os
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.production')

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from app.middleware import JWTAuthMiddleware

# Import websocket_urlpatterns lazily
def get_websocket_urlpatterns():
    from app.routing import websocket_urlpatterns
    return websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(get_websocket_urlpatterns())
    ),
})