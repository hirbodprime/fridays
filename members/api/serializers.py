from rest_framework import serializers
from members.models import Class, Attendance,PaymentImage
from django.contrib.auth import get_user_model
User = get_user_model()

class PaymentImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = PaymentImage
        fields = ['image', 'amount', 'created_at']

    def get_image(self, obj):
        if obj.image:
            return f"https://hirbots.com/fridays{obj.image.url}"
        return None
class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name','profile_image']  # Adjust fields as needed for the user
    def get_profile_image(self, obj):
        if obj.profile_image:
            return f"https://hirbots.com/fridays{obj.profile_image.url}"
        return None
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
        fields = ['id','title', 'description', 'date', 'charge_amount', 'is_available_this_week', 'image', 'present_attendees','finished']

    def get_present_attendees(self, obj):
        # Filter attendees marked as 'present' for this class
        attendees = Attendance.objects.filter(class_attended=obj, status='present')
        return AttendanceSerializer(attendees, many=True).data
