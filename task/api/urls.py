from django.urls import path
from .views import TaskViewSet

urlpatterns = [
    path('tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list-create'),
    path('task/<int:pk>/', TaskViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',  # Handle PATCH requests
        'delete': 'destroy'
    }), name='task-detail'),
]
