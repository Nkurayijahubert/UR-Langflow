from django.utils import timezone
import logging
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

@database_sync_to_async
def get_user(token_key):
    try:
        access_token = AccessToken(token_key)
        
        # Check if token is expired
        if access_token['exp'] < timezone.now().timestamp():
            logger.info("Token has expired")
            return AnonymousUser()
        
        # Get user from token payload
        user_id = access_token['user_id']
        try:
            user = User.objects.get(id=user_id)
            return user, None
        except User.DoesNotExist:
            logger.error(f"User with id {user_id} not found")
            return AnonymousUser(), f"User not found"
        
    except (TokenError, InvalidToken) as e:
        logger.error(f"Token error: {str(e)}")
        return AnonymousUser(), str(e)

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):

        headers = dict(scope['headers'])
        logger.info(f"Headers: {headers}")
        
        auth_header = headers.get(b'authorization', b'').decode()
        logger.info(f"Auth header: {auth_header}")
        
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            logger.info(f"Token extracted: {token[:10]}...")  # Log first 10 chars of token for security
            user, error = await get_user(token)
            if error:
                scope['user'] = AnonymousUser()
                scope['auth_error'] = error
            else:
                scope['user'] = user
            logger.info(f"User authenticated: {scope['user']}")
        else:
            scope['user'] = AnonymousUser()
            scope['auth_error'] = "No valid token provided"
            logger.info("No valid token provided, user is anonymous")
        
        return await super().__call__(scope, receive, send)