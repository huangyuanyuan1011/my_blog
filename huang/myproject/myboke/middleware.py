from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from .models import User


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        uid = request.session.get('userid')
        if uid is not None:
            user = User.objects.get(id=uid)
            request.user = user