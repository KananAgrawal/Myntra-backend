from rest_framework import serializers
from account.models import User
from .models import *

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'myntra_credits']

class BlogSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'likes']

    def get_type(self, obj):
        return 'blog'
    
class PostSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'likes']

    def get_type(self, obj):
        return 'post'
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
