from rest_framework import status, permissions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset()).distinct()
        obj = get_object_or_404(queryset, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.is_anonymous or request.user not in instance.assigned_users.all():
            return Response({"error": "You do not have permission to view this task."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        if not user.premium:
            return Response({"error": "Only premium users can create tasks."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            task = serializer.save(created_by=user)
            
            # If 'assign_all' is in request, assign all users to the task
            if request.data.get('assign_all') == True:
                task.assigned_users.set(CustomUser.objects.all())
            task.save()

            # Return success: true and data in a 'data' key
            return Response({
                'success': True,
                'data': serializer.data  # Wrap serialized data in 'data' key
            }, status=status.HTTP_201_CREATED)
        
        else:
            # Return validation errors
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Task.objects.none()  # No tasks for anonymous users
        # Return tasks where the user is assigned or is the creator
        return Task.objects.filter(assigned_users=user)

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

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user.is_anonymous or task.created_by != request.user:
            return Response({"error": "You do not have permission to delete this task."}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(task)
        return Response(status=status.HTTP_204_NO_CONTENT)
