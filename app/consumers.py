from datetime import datetime
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from app.langflow_integration import langflow_config

logger = logging.getLogger(__name__)

class LangflowConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from django.contrib.auth.models import AnonymousUser

        user = self.scope['user']
        logger.info(f"Attempting to connect. User: {self.scope['user']}")
        if isinstance(user, AnonymousUser):
            logger.info("Rejecting anonymous user")
            await self.accept()
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Authentication failed. Token may have expired.',
                'code': 401
            }))

            await self.close()
        else:
            logger.info(f"Accepting connection for user: {self.scope['user']}")
            
            await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected. Close code: {close_code}")

    async def receive(self, text_data):
        logger.info(f"Received data: {text_data[:50]}...")
        try:
            data = json.loads(text_data)
            question = data.get('message')
            if question:
                logger.info(f"Processing question: {question}")
                response = await self.process_langflow(question)
                logger.info(f"Received response from process_langflow: {response}")

                # Extract text and timestamp from the response
                text_value, timestamp = self.extract_response_data(response)

                await self.send(text_data=json.dumps({
                    'type': 'response',
                    'message': text_value,
                    'timestamp': timestamp
                }))

                # Access the first element of the response list
                # run_output = response[0]
                
                # # Access the 'outputs' list within the run_output dictionary
                # outputs = run_output.outputs[0]
                # if outputs:
                #     # Access the first output's results
                #     result_data = outputs[0].get('results', {})
                #     # Access the 'message' data
                #     message_data = result_data.results['message']
                #     text_value = message_data.data['text']
                #     timestamp = message_data.data.get('timestamp', '')

                #     if not timestamp:
                #         timestamp = datetime.now().isoformat()

                #     await self.send(text_data=json.dumps({
                #         'type': 'response',
                #         'message': text_value,
                #         'timestamp': timestamp
                #     }))
                # else:
                #     logger.warning("No outputs in the response")
                #     await self.send(text_data=json.dumps({
                #         'type': 'error',
                #         'message': 'No outputs in the response',
                #         'timestamp': datetime.now().isoformat()
                #     }))
            else:
                logger.warning("No question provided")
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'No question provided',
                    'timestamp': datetime.now().isoformat()
                }))
        except json.JSONDecodeError:
            logger.error("Invalid JSON format")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format',
                'timestamp': datetime.now().isoformat()
            }))
        except Exception as e:
            logger.exception(f"An error occurred while processing the request: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'An error occurred while processing your request: {str(e)}',
                'timestamp': datetime.now().isoformat()
            }))

    def extract_response_data(self, response):
        try:
            if isinstance(response, list) and len(response) > 0:
                run_outputs = response[0]
                if hasattr(run_outputs, 'outputs') and len(run_outputs.outputs) > 0:
                    result_data = run_outputs.outputs[0]
                    if hasattr(result_data, 'results') and 'message' in result_data.results:
                        message = result_data.results['message']
                        text = message.text
                        timestamp = message.timestamp
                        return text, timestamp
            
            # If we couldn't extract the data as expected, return a default response
            logger.warning(f"Unexpected response structure: {response}")
            return "Unexpected response structure", datetime.now().isoformat()
        except Exception as e:
            logger.exception(f"Error extracting response data: {str(e)}")
            return f"Error extracting response: {str(e)}", datetime.now().isoformat()
    
    @sync_to_async
    def process_langflow(self, question):
        # Process the question using Langflow
        result = langflow_config.run_flow({"question": question})
        return result  