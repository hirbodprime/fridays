from rest_framework import serializers
from members.models import Class, Attendance
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name','profile_image']  # Adjust fields as needed for the user

# Modify the AttendanceSerializer to include user data
class AttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nest UserSerializer for the user field

    class Meta:
        model = Attendance
        fields = ['user', 'status', 'timestamp']  # Adjust fields as needed

class ClassSerializer(serializers.ModelSerializer):
    # Use a SerializerMethodField to include custom attendee data
    present_attendees = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ['title', 'description', 'date', 'charge_amount', 'is_available_this_week', 'image', 'present_attendees']

    def get_present_attendees(self, obj):
        # Filter attendees marked as 'present' for this class
        attendees = Attendance.objects.filter(class_attended=obj, status='present')
        return AttendanceSerializer(attendees, many=True).data
