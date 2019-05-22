from django.utils.deprecation import MiddlewareMixin

from .utils import url_is_blocked
from .views import unavailable_for_legal_reasons


class FahrenheitMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not url_is_blocked(request, request.path_info):
            return self.get_response(request)
        return unavailable_for_legal_reasons(request)
