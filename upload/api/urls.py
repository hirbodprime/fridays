from django.urls import path
from .views import CreateVideoView, ClassVideosView, AllVideosView

urlpatterns = [
    path('video/create/<int:class_id>/', CreateVideoView.as_view(), name='create-video'),
    path('video/<int:class_id>/', ClassVideosView.as_view(), name='class-videos'),
    path('videos/', AllVideosView.as_view(), name='all-videos'),
]
