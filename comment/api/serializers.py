from rest_framework import serializers
from comment.models import Comment, Quote


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'class_ref', 'date_added']
        read_only_fields = ['user', 'class_ref']  # Make class_ref read-only

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'text', 'user', 'class_ref', 'date_added']
        read_only_fields = ['user', 'class_ref']  # Make class_ref read-only
