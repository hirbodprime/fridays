from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from task.models import Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from task.models import Task
from account.models import CustomUser
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset()).distinct()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        print(obj)
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.premium:
            return Response({"error": "Only premium users can create tasks."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            task = serializer.save(created_by=user)
            # If 'assign_all' is in request, assign all users to the task
            if request.data.get('assign_all'):
                task.assigned_users.set(CustomUser.objects.all())
            task.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        user = self.request.user
        # Return tasks where the user is assigned or is the creator
        return Task.objects.filter(assigned_users=user) | Task.objects.filter(created_by=user)
        # return Task.objects.filter(assigned_users=user) 

    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()
        assign_all = request.data.get('assign_all', False)

        # If assign_all is True, assign the task to all users
        if assign_all:
            task.assigned_users.set(CustomUser.objects.all())
            task.save()
            return Response({
                'status': 'success',
                'message': 'Task assigned to all users.'
            }, status=status.HTTP_200_OK)

        # Continue with the standard partial update if assign_all is not True
        return super(TaskViewSet, self).partial_update(request, *args, **kwargs)