from django.urls import path,include
from django.contrib.auth import views as auth_views
from account.views import *

urlpatterns = [
    path('Signup/',SignupView.as_view(),name='signup'),
    path('verify/', EmailVerificationView.as_view(), name='verify_email'),
    path('login/', LoginAPIView.as_view(),name='login'),
    path('logout/', LogoutAPIView.as_view(), name="logout"),



]