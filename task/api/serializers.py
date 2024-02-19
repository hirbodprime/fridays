from rest_framework import serializers
from task.models import Task
from account.models import CustomUser

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'deadline', 'created_by', 'assigned_users']
        extra_kwargs = {
            'created_by': {'read_only': True},
        }
