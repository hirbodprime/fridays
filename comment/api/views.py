from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
import datetime
from django.utils import timezone

from comment.models import Comment, Quote
from members.models import Class

from .serializers import CommentSerializer, QuoteSerializer

class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, class_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, class_ref_id=class_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListCommentView(APIView):
    def get(self, request, class_id):
        comments = Comment.objects.filter(class_ref_id=class_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CreateQuoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, class_id):
        serializer = QuoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, class_ref_id=class_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListQuoteView(APIView):
    def get(self, request, class_id):
        quotes = Quote.objects.filter(class_ref_id=class_id)
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)