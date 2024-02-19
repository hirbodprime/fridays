from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassViewSet, ToggleAttendanceView

router = DefaultRouter()
router.register(r'classes', ClassViewSet, basename='class')  # Specify the basename here

urlpatterns = [
    path('toggle-attendance/<int:pk>/', ToggleAttendanceView.as_view(), name='toggle-attendance'),
    path('', include(router.urls)),
]
