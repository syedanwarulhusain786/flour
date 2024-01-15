# middleware.py

from threading import current_thread
from django.utils.deprecation import MiddlewareMixin

class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        current_user = getattr(request, 'user', None)
        setattr(current_thread(), '_current_user', current_user)
