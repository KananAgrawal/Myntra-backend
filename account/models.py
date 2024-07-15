from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,email,mobile_number,full_name,country,social_media,gender,password=None):
        if not mobile_number:
            raise ValueError("User must have a mobile number")
        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            full_name=full_name,
            gender=gender,
            country=country,
            social_media=social_media,
            password=password
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self,email,mobile_number,full_name,country,gender,password=None,social_media=None):
        if not mobile_number:
            raise ValueError("User must have a mobile number")
        if not email:
            raise ValueError("User must have an email address")
        user=self.create_user(
            mobile_number=mobile_number,
            password=password,
            email=email,
            full_name=full_name,
            gender=gender,
            country=country,
            social_media=social_media,
            
        )
        user.is_admin = True
        user.isVerified=True
        user.save(using=self._db)
        return user
    
class User(AbstractBaseUser):
    full_name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    mobile_number=models.CharField(max_length=10,unique=True)
    gender=models.CharField(max_length=10,null=True)
    country=models.CharField(max_length=50,null=True)
    social_media=models.URLField(blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    isVerified=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)

    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['mobile_number','full_name','country','gender']

    def __str__(self):
        return self.full_name
        
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
        
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }




