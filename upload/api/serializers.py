from rest_framework import serializers
from django.conf import settings
from upload.models import Video

class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'file', 'class_ref', 'uploaded_at']
        read_only_fields = ['class_ref']

class VideoListSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    class Meta:
        model = Video
        fields = ['id', 'title', 'file', 'class_ref', 'uploaded_at']
        read_only_fields = ['class_ref']

    def get_file(self, obj):
        if obj.file:
            return f"{settings.BASE_URL}{obj.file.url}"  # Use 'BASE_URL' here
        return None