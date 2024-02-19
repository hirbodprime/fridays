from rest_framework import serializers
from members.models import Class, Attendance

class AttendanceSerializer(serializers.ModelSerializer):
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
