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

from upload.models import Video
from .serializers import VideoListSerializer, VideoCreateSerializer

class CreateVideoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, class_id):
        serializer = VideoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(class_ref_id=class_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ClassVideosView(APIView):
    def get(self, request, class_id):
        videos = Video.objects.filter(class_ref_id=class_id)
        serializer = VideoListSerializer(videos, many=True)
        return Response(serializer.data)

class AllVideosView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        serializer = VideoListSerializer(videos, many=True)
        return Response(serializer.data)
