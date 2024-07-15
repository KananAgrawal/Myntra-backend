from account.models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth 
from rest_framework.exceptions import AuthenticationFailed


class SignupSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password=serializers.CharField(write_only=True,required=True)


    class Meta:
        model=User
        fields = ['id','email','mobile_number','full_name','gender','country','social_media','password','confirm_password']
        extra_kwargs={
            'password':{'write_only':True},
        }


    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self,validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)
    


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
    

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)  



class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    password=serializers.CharField(max_length=68,write_only=True)
    tokens=serializers.CharField(read_only=True)
    class Meta:
        model=User
        fields=['email','password','tokens'] 
    def validate(self,attrs):
        email=attrs.get('email','')
        password=attrs.get('password','')

        user=auth.authenticate(email=email,password=password)
      
        if not user:
            raise AuthenticationFailed('Email or Password is Incorrect!')
        if not user.isVerified:
            raise AuthenticationFailed('Email is not Verified!')
        return {
            'mobile_number':user.mobile_number,
            'full_name':user.full_name,
            'email':user.email,
            'tokens':user.tokens
        }
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self,attrs):
        self.token= attrs['refresh']
        return attrs


    def save(self,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        
        
        except TokenError:
            self.fail('bad_token')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','mobile_number','email','full_name','country','social_media','gender']
