# from mailing.consumers import routing
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import mailing.consumers
import mailing.consumers.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MailServer.settings')

asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        'http': asgi_app,
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(mailing.consumers.routing.urlpatterns)
            )
        )
    }
)
