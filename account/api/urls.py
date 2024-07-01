from django.urls import path,include
from . import views as v
urlpatterns = [
    path('login/', v.LoginView.as_view(), name='login'),
    path('signup/', v.SignupView.as_view(), name='signup'),
    path('user/profile/', v.UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', v.UserProfileUpdateAPIView.as_view(), name='user-update'),
    path('profile/<str:username>/', v.UserProfileAPIView.as_view(), name='user-profile'),
    path('wallet/<int:user_id>/', v.WalletAPIView.as_view(), name='wallet-detail'),
    path('payment-image/', v.PaymentImageView.as_view(), name='payment-image-upload'),
    path('upload-profile-picture/', v.UploadProfilePicture.as_view(), name='upload_profile_picture'),
    path('users/', v.UserListView.as_view(), name='users-list'),

]
