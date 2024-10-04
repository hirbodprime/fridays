from rest_framework import serializers
from task.models import Task
from account.models import CustomUser
from account.api.serializers import UserProfileSerializer

from datetime import timedelta
from django.utils import timezone


class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.all(), required=False
    )
    deadline = serializers.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'],
        format='%Y-%m-%dT%H:%M:%S%z',  # The format you want to output
        required=False
    )
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'deadline', 'created_by', 'assigned_users']
        extra_kwargs = {
            'created_by': {'read_only': True},
        }

    def validate(self, data):
        assign_all = self.context['request'].data.get('assign_all', False)
        assigned_users = data.get('assigned_users')

        if assign_all:
            # If assign_all is True, no need to check for assigned_users.
            if assigned_users:
                raise serializers.ValidationError({
                    'assigned_users': 'You cannot set assigned_users when assign_all is true.'
                })
        elif not assigned_users:
            # If assign_all is False, assigned_users is required.
            raise serializers.ValidationError({
                'assigned_users': 'This field is required.'
            })
        return data
