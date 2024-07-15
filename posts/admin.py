from django.contrib import admin
from .models import *

# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'get_like_count')
    search_fields = ('title', 'description')

    def get_like_count(self, obj):
        return obj.likes.count()
    get_like_count.short_description = 'Likes'

class PostAdmin(admin.ModelAdmin):
    list_display = ('caption', 'created_at', 'get_like_count')
    search_fields = ('caption',)

    def get_like_count(self, obj):
        return obj.likes.count()
    get_like_count.short_description = 'Likes'

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at')
    search_fields = ('text',)
    list_filter = ('created_at',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'myntra_credits')
    search_fields = ('user__username',)

admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
