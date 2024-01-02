# """
# ASGI config for erp project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp.settings')

# application = get_asgi_application()


# erp/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import accounting.routing  # Import routing from accounting app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": accounting.routing.application,
})

