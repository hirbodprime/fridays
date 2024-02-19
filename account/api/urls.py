from django.urls import path,include
from . import views as v
urlpatterns = [
    path('login/', v.LoginView.as_view(), name='login'),

]
