from django.urls import path,include
from . import views as v
urlpatterns = [
    path('login/', v.LoginView.as_view(), name='login'),
    path('signup/', v.SignupView.as_view(), name='signup'),
    path('profile/update/', v.UserProfileUpdateAPIView.as_view(), name='user-update'),
    path('profile/<str:username>/', v.UserProfileAPIView.as_view(), name='user-profile'),

]
