# UR-langflow

This project provides a Django backend with WebSocket support and JWT-based authentication. The backend is designed to work with a locally deployed, finetuned Large Language Model (LLM) to assist students pursuing undergraduate programs at the University of Rwanda.

## Features

- JWT-based authentication
- WebSocket support for real-time communication
- Integration with a locally deployed LLM

## Setup

### Prerequisites

- Docker and Docker Swarm
- Python 3.10
- Django
- PostgreSQL

### Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
ASTRA_DB_APPLICATION_TOKEN=your_astra_db_application_token
ASTRA_DB_API_ENDPOINT=your_astra_db_api_endpoint
```

### Docker Setup

1. **Initialize Docker Swarm:**

   ```bash
   docker swarm init
   ```

2. **Generate Password and Secret Key:**

   ```bash
   echo "WVcc2bJ5m1gB5iSLRgPT" | docker secret create ibl_db_password -
   echo "F5D24B33AF85FD7FE91D3FB2B624E" | docker secret create ibl_django_secret_key -
   ```

3. **Docker Login:**

   ```bash
   docker login
   ```

4. **Build Docker Images:**

   ```bash
   docker build -f Dockerfile.web -t nkurayijah/ibl_web:latest .
   docker build -f Dockerfile.websocket -t nkurayijah/ibl_websocket:latest .
   ```

5. **Push Images to the Registry:**

   ```bash
   docker push nkurayijah/ibl_web:latest
   docker push nkurayijah/ibl_websocket:latest
   ```

6. **Deploy the Stack:**

   ```bash
   docker stack deploy -c docker-compose.yml ibl_app
   ```

### Testing the WebSocket with Postman

You can test the WebSocket connection using Postman. Follow these steps:

1. **Open Postman**:

   - Launch Postman on your system.

2. **Create a New WebSocket Request**:

   - Click "New" > "WebSocket Request."
   - Enter the WebSocket URL: `ws://localhost:8001/ws/chat/`.
   - Click "Connect" to establish the connection.

3. **Set the Authorization Header**:

   - After connecting, navigate to the "Headers" section.
   - Add the following header:
     - **Key**: `Authorization`
     - **Value**: `Bearer your_jwt_token`
   - Replace `your_jwt_token` with your actual JWT token.

4. **Send a Message**:

   - In the message field, enter the following JSON structure:
     ```json
     {
       "message": "your question"
     }
     ```
   - Click "Send" to send the message to the server.

5. **View the Response**:

   - The server's response will appear in the response section of Postman.

6. **Close the WebSocket Connection**:
   - After testing, click "Disconnect" to close the WebSocket connection.

### Example WebSocket Request in Postman

- **URL**: `ws://localhost:8001/ws/chat/`
- **Headers**:
  - `Authorization: Bearer your_jwt_token`
- **Message Body**:
  ```json
  {
    "message": "How does this work?"
  }
  ```

### Obtain JWT Token

1. **Register**:

   - Register by sending a POST request to `http://localhost:80/api/register/` with your username and password.

2. **Get the Token**:
   - Obtain the token by sending a POST request to `http://localhost:80/api/token/` using the same credentials.

### Contact

For any issues or questions, please contact [Nkurayijah Hubert](mailto:nkurayijah@gmail.com).
