from django.urls import path
from app.views import *

urlpatterns = [
    path('', home),
    path('api/register/', RegisterView.as_view(), name='register'),
    # path('api/agent/', AgentView.as_view(), name='agent'),
]