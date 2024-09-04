import json
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.test import TestCase
from app.consumers import LangflowConsumer
from unittest.mock import patch
import pytest
from asgiref.sync import sync_to_async

from django.contrib.auth.models import AnonymousUser

User = get_user_model()

class MockMessage:
    def __init__(self, text, timestamp):
        self.text = text
        self.timestamp = timestamp

class MockResultData:
    def __init__(self, text, timestamp):
        self.results = {'message': MockMessage(text, timestamp)}

class MockRunOutputs:
    def __init__(self, text, timestamp):
        self.outputs = [MockResultData(text, timestamp)]

@pytest.mark.asyncio
class TestLangflowConsumer(TestCase):
    @sync_to_async
    def create_user(self, username, password):
        return User.objects.create_user(username=username, password=password)

    async def test_connect_authenticated(self):
        user = await self.create_user('testuser', '12345')
        communicator = WebsocketCommunicator(LangflowConsumer.as_asgi(), "/ws/langflow/")
        communicator.scope["user"] = user
        connected, _ = await communicator.connect()
        assert connected
        await communicator.disconnect()

    async def test_connect_unauthenticated(self):
        communicator = WebsocketCommunicator(LangflowConsumer.as_asgi(), "/ws/langflow/")
        communicator.scope["user"] = AnonymousUser()
        connected, _ = await communicator.connect()
        
        assert connected, "WebSocket connection failed"
        
        response = await communicator.receive_json_from()
        print("Received response:", response)  # Add this line for debugging
        
        assert response["type"] == "error"
        assert response["message"] == "Authentication failed. Token may have expired."
        assert response["code"] == 401
        
        # Check if the connection is closed after sending the error message
        closed = await communicator.receive_output()
        assert closed['type'] == 'websocket.close'

        await communicator.disconnect()

    @patch('app.langflow_integration.langflow_config.run_flow')
    async def test_receive_valid_message(self, mock_run_flow):
        mock_run_flow.return_value = [MockRunOutputs("Test response", "2023-01-01 00:00:00")]

        user = await self.create_user('testuser', '12345')
        communicator = WebsocketCommunicator(LangflowConsumer.as_asgi(), "/ws/langflow/")
        communicator.scope["user"] = user
        connected, _ = await communicator.connect()
        assert connected

        await communicator.send_json_to({"message": "Test question"})
        response = await communicator.receive_json_from()

        print("Received response:", response)

        assert "type" in response, "Response does not contain 'type' key"
        assert "message" in response, "Response does not contain 'message' key"
        assert "timestamp" in response, "Response does not contain 'timestamp' key"
        
        assert response["type"] == "response", f"Expected type 'response', but got '{response.get('type')}'"
        assert response["message"] == "Test response", f"Expected message 'Test response', but got '{response.get('message')}'"
        assert response["timestamp"] == "2023-01-01 00:00:00", f"Expected timestamp '2023-01-01 00:00:00', but got '{response.get('timestamp')}'"

        await communicator.disconnect()

    @patch('app.langflow_integration.langflow_config.run_flow')
    async def test_receive_unexpected_response(self, mock_run_flow):
        mock_run_flow.return_value = [{"unexpected": "structure"}]

        user = await self.create_user('testuser', '12345')
        communicator = WebsocketCommunicator(LangflowConsumer.as_asgi(), "/ws/langflow/")
        communicator.scope["user"] = user
        connected, _ = await communicator.connect()
        assert connected

        await communicator.send_json_to({"message": "Test question"})
        response = await communicator.receive_json_from()

        print("Received response:", response)

        assert response["type"] == "response"
        assert response["message"] == "Unexpected response structure"
        assert "timestamp" in response

        await communicator.disconnect()

    async def test_receive_invalid_json(self):
        user = await self.create_user('testuser', '12345')
        communicator = WebsocketCommunicator(LangflowConsumer.as_asgi(), "/ws/langflow/")
        communicator.scope["user"] = user
        connected, _ = await communicator.connect()
        assert connected

        await communicator.send_to(text_data="Invalid JSON")
        response = await communicator.receive_json_from()

        assert response["type"] == "error"
        assert response["message"] == "Invalid JSON format"

        await communicator.disconnect()