from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassViewSet, ToggleAttendanceView, ClassHistoryListView, AttendedClassesListView,ClassCreateAPIView,ClassUpdateAPIView,UserPaymentImageListView,UpdateWalletBalanceView

router = DefaultRouter()
router.register(r'classes', ClassViewSet, basename='class')  # Specify the basename here

urlpatterns = [
    path('toggle-attendance/<int:pk>/', ToggleAttendanceView.as_view(), name='toggle-attendance'),
    path('', include(router.urls)),
    path('class-history/', ClassHistoryListView.as_view(), name='class-history-list'),
    path('attended/', AttendedClassesListView.as_view(), name='attended-classes'),
    path('class/create/', ClassCreateAPIView.as_view(), name='class-create'),
    path('class/update/<int:pk>/', ClassUpdateAPIView.as_view(), name='class-update'),
    path('payment-images/', UserPaymentImageListView.as_view(), name='payment-images'),
    path('update-wallet/<int:user_id>/', UpdateWalletBalanceView.as_view(), name='update-wallet'),

]
