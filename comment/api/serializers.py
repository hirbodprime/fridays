from rest_framework import serializers
from comment.models import Comment, Quote
from account.api.serializers import UserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'text', 'class_ref', 'date_added','user']
        read_only_fields = ['user', 'class_ref']  # Make class_ref read-only
    def get_user(self, obj):
        # Assuming your Comment model has a field named 'user' that links to the CustomUser model
        user = obj.user
        return UserProfileSerializer(user).data
class QuoteSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Quote
        fields = ['id', 'text', 'user', 'class_ref', 'date_added','user']
        read_only_fields = ['user', 'class_ref']  # Make class_ref read-only
    def get_user(self, obj):
        # Assuming your Comment model has a field named 'user' that links to the CustomUser model
        user = obj.user
        return UserProfileSerializer(user).data