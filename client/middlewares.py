from datetime import datetime, timedelta
from typing import Callable

from django.contrib.auth.models import User
from pytz import timezone as tz
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response


def logout_on_timeout_middleware(get_response: Callable) -> Callable:
    def middleware(request: HttpRequest) -> HttpResponse:
        response = get_response(request)
        if request.user.is_authenticated and not request.user.is_staff:
            delta = datetime.now() - request.user.last_login.replace(tzinfo=None)
            if delta.days >= settings.LOGOUT_TIMEOUT:
                try:
                    request.user.auth_token.delete()
                except User.auth_token.RelatedObjectDoesNotExist:
                    pass
                response['error'] = 'token expired'
                return JsonResponse({'error': 'token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        return response
    return middleware