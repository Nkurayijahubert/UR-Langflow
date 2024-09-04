from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from app.middleware import get_user, JWTAuthMiddleware
from unittest.mock import AsyncMock, patch
from django.utils import timezone
import pytest

User = get_user_model()

class MiddlewareTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    @pytest.mark.asyncio
    async def test_get_user_valid_token(self):
        token = AccessToken.for_user(self.user)
        user, error = await get_user(str(token))
        assert user == self.user
        assert error is None

    @pytest.mark.asyncio
    async def test_get_user_expired_token(self):
        token = AccessToken.for_user(self.user)
        token.set_exp(lifetime=-timezone.timedelta(days=1))
        user = await get_user(str(token))
        assert user.is_anonymous

    @pytest.mark.asyncio
    async def test_get_user_invalid_token(self):
        user = await get_user("invalid_token")
        assert user.is_anonymous

    @pytest.mark.asyncio
    @patch('app.middleware.get_user')
    async def test_jwt_auth_middleware_valid_token(self, mock_get_user):
        mock_get_user.return_value = (self.user, None)
        middleware = JWTAuthMiddleware(AsyncMock())
        scope = {
            'headers': [(b'authorization', b'Bearer valid_token')]
        }
        await middleware(scope, AsyncMock(), AsyncMock())
        assert scope['user'] == self.user

    @pytest.mark.asyncio
    async def test_jwt_auth_middleware_no_token(self):
        middleware = JWTAuthMiddleware(AsyncMock())
        scope = {'headers': []}
        await middleware(scope, AsyncMock(), AsyncMock())
        assert scope['user'].is_anonymous
        assert scope['auth_error'] == "No valid token provided"