from django.urls import path
from .views import TaskViewSet

# Define the URL patterns directly
urlpatterns = [
    path('tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list-create'),
    path('task/<int:pk>/', TaskViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',  # Add this line to handle PATCH requests
            'delete': 'destroy'
        }), name='task-detail'),
]
