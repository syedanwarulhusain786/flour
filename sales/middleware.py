# middleware.py
from django.utils.deprecation import MiddlewareMixin
import threading

_local = threading.local()

class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _local.current_user = request.user