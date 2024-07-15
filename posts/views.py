from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Blog, Post, Comment, UserProfile
from .serializers import BlogSerializer, PostSerializer, CommentSerializer, UserProfileSerializer
from itertools import chain
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class BlogCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Create a new blog",
        request_body=BlogSerializer,
        responses={201: BlogSerializer}
    )

    def post(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Create a new post",
        request_body=PostSerializer,
        responses={201: PostSerializer}
    )

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class UserProfileView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

@api_view(['POST'])
def like_blog(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if user in blog.likes.all():
        blog.likes.remove(user)
    else:
        blog.likes.add(user)
        if blog.likes.count() % 15 == 0:
            user_profile = UserProfile.objects.get(user=blog.user)
            user_profile.myntra_credits += 1
            user_profile.save()

    blog.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def like_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        if post.likes.count() % 15 == 0:
            user_profile = UserProfile.objects.get(user=post.user)
            user_profile.myntra_credits += 1
            user_profile.save()

    post.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def home_view(request):
    blogs = Blog.objects.all()
    posts = Post.objects.all()
    combined = sorted(
        chain(blogs, posts), 
        key=lambda instance: instance.created_at, 
        reverse=True
    )
    
    # Serializing both Blog and Post objects using their respective serializers
    data = []
    for item in combined:
        if isinstance(item, Blog):
            serializer = BlogSerializer(item)
        elif isinstance(item, Post):
            serializer = PostSerializer(item)
        data.append(serializer.data)
    
    return Response(data)
