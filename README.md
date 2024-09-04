# UR-langflow

UR-langflow is a project that integrates Docker Swarm with Django REST Framework to expose a WebSocket interface using Langflow. The WebSocket prompts an agent that leverages a locally deployed, finetuned Large Language Model (LLM) and a custom Langflow tool to answer questions. To ensure security, the WebSocket is accessible only via token-based authentication.

## Features

- **WebSocket Interface**: Exposes a WebSocket endpoint that interacts with Langflow.
- **Custom Langflow Tool**: Integrates a custom tool into Langflow for enhanced capabilities.
- **Locally Deployed LLM**: Uses a finetuned LLM deployed locally.
- **Token-Based Authentication**: Secure access to the WebSocket via JWT tokens.

## Installation

### Prerequisites

- Docker & Docker Swarm
- Python 3.8+
- Django 4.0+
- [Langflow](https://github.com/langflow/langflow)

### Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Nkurayijahubert/UR-langflow.git
   cd UR-langflow
   ```

2. **Environment Setup**

   Create a `.env` file in the root directory with the following environment variables:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ASTRA_DB_APPLICATION_TOKEN=your_astra_db_application_token
   ASTRA_DB_API_ENDPOINT=your_astra_db_api_endpoint
   ```

3. **Build Docker Containers**

   - **Initialize Docker Swarm**:

     ```bash
     docker swarm init
     ```

   - **Generate Password and Secret Key**:

     ```bash
     echo "WVcc2bJ5m1gB5iSLRgPT" | docker secret create ibl_db_password -
     echo "F5D24B33AF85FD7FE91D3FB2B624E" | docker secret create ibl_django_secret_key -
     ```

   - **Docker Login**:

     ```bash
     docker login
     ```

   - **Build Images**:

     ```bash
     docker build -f Dockerfile.web -t username/ibl_web:latest .
     docker build -f Dockerfile.websocket -t username/ibl_websocket:latest .
     ```

   - **Push Images to the Registry**:

     ```bash
     docker push username/ibl_web:latest
     docker push username/ibl_websocket:latest
     ```

   - **Deploy the Stack**:

     ```bash
     docker stack deploy -c docker-compose.yml ibl_app
     ```

4. **Apply Migrations**

   Once the services are running, apply the Django migrations:

   ```bash
   docker exec -it <django_service_container_id> python manage.py migrate
   ```

5. **Create a Superuser**

   Create a Django superuser to access the admin panel:

   ```bash
   docker exec -it <django_service_container_id> python manage.py createsuperuser
   ```

### Running the Project

Once everything is set up, the WebSocket interface should be accessible via the designated endpoint. Authentication is required, so be sure to obtain a JWT token first.

## Usage

### Authentication

1. **Register a User**

   Send a POST request to the `/api/register/` endpoint with your credentials to register:

   ```json
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

2. **Obtain a Token**

   Once registered, send a POST request to the `/api/token/` endpoint with your credentials to obtain a JWT token:

   ```json
   {
     "username": "your_username",
     "password": "your_password"
   }
   ```

3. **Access WebSocket**

   Use the obtained token to authenticate WebSocket connections at `ws://localhost:8001/ws/chat/`:

   ```javascript
   const socket = new WebSocket("ws://localhost:8001/ws/chat/");
   socket.onopen = function (event) {
     socket.send(
       JSON.stringify({
         type: "authenticate",
         token: "your_jwt_token",
       })
     );
   };
   ```

### Interacting with the Agent

Once authenticated, send a message to the WebSocket to interact with the Langflow agent:

```json
{
  "message": "your_question_here"
}
```

The agent will process your request using the locally deployed LLM and the custom Langflow tool.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Make sure to follow the coding standards and write tests where applicable.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries or support, please reach out to [Nkurayijah Hubert](mailto:nkurayijah@gmail.com).
