from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .langflow_integration import langflow_config

from .serializers import UserSerializer
from django.shortcuts import render
from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AgentView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request):

#         #get the username of the authenticated user
#         username = request.user.username

#         question = request.data.get('question')
#         if not question:
#             return Response({"error": "No question provided"}, status=400)
        
#         # Run the Langflow agent
#         response_data = langflow_config.run_flow({"question": question})
#         print("response data", response_data)
#         # Access the first RunOutputs element
#         run_output = response_data[0]
        
#         # Access the first ResultData element within outputs
#         result_data = run_output.outputs[0]

#         # Access the 'text' and 'timestamp' field from the results
#         message_data = result_data.results['message']
#         text_value = message_data.data['text']
#         timestamp = message_data.data['timestamp']

#         return Response({"text": text_value, "timestamp": timestamp})