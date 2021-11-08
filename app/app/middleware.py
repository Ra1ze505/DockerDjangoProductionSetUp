from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async, close_old_connections
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework import exceptions
from jwt import decode as jwt_decode
from django.conf import settings
import logging

from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()

        headers = {key: value for key, value in scope['headers']}

        auth_header = headers.get(b'authorization', '').split()

        if not auth_header or auth_header[0].lower() != b'jwt' or len(auth_header) != 2:
            return exceptions.AuthenticationFailed('Invalid token')
        # Get the token
        token = headers[b'authorization'].decode().split()[1]

        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            return None
        else:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            scope['user'] = await get_user(decoded_data['user_id'])
        return await self.inner(scope, receive, send)


def JWTAuthMiddlewareStack(app):
    return TokenAuthMiddleware(AuthMiddlewareStack(app))

