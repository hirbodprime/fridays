from django.urls import path
from .views import TaskViewSet,UserCreatedTasksView

urlpatterns = [
    path('tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list-create'),
    path('task/<int:pk>/', TaskViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',  # Handle PATCH requests
        'delete': 'destroy'
    }), name='task-detail'),
    path('user-created-tasks/', UserCreatedTasksView.as_view(), name='user-created-tasks'),

]
