from django.shortcuts import render
from account.models import *
from account.serializers import *
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import Util
from django.conf import settings
import random
from account.renderers import UserRenderer
import jwt
from rest_framework import exceptions as rest_exceptions, response, decorators as rest_decorators, permissions as rest_permissions
from rest_framework_simplejwt import tokens, views as jwt_views, serializers as jwt_serializers, exceptions as jwt_exceptions
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.sites.shortcuts import get_current_site
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        otp = str(random.randint(100000, 999999))
        user.otp=otp
        user.save()
        user_data = serializer.data
        user_email = User.objects.get(email=user_data['email'])
        token = str(RefreshToken.for_user(user_email).access_token)
        current_site = get_current_site(request).domain
        email=request.data.get('email')
        
        email_body= 'Greeting!'+user_email.full_name + \
        'OTP for your email verification is given below: \n' + otp
        data = {'email_body': email_body, 'to_email': user_email.email,
                'email_subject': 'OTP for Verification'}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)
    

# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer


class EmailVerificationView(views.APIView):

    @swagger_auto_schema(
        request_body=EmailVerificationSerializer,
        responses={
            200: 'Email verified successfully',
            400: 'Invalid OTP or Bad Request',
            404: 'User not found'
        }
    )
        
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                if user.otp == otp:
                    user.isVerified = True
                    user.save()
                    return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email', '')
        password = serializer.validated_data.get('password', '')

        print(f"Attempting to authenticate user with email: {email}")
        
        user = auth.authenticate(email=email, password=password)
        if user:
            print(f"User found: {user}")
        else:
            print("User not found")
            try:
                user_in_db = User.objects.get(email=email)
                print(f"User in DB: {user_in_db}, Password: {password}, Hashed Password: {user_in_db.password}")
            except User.DoesNotExist:
                print("User with given email does not exist in the database.")
        
        if user and user.isVerified:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            raise rest_exceptions.AuthenticationFailed("Email or Password is incorrect or user is not verified!")

class LogoutAPIView(generics.GenericAPIView):
    serializer_class=LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        logout(request)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)