from django.contrib import admin
from .models import UserProfile, Post, Comment, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'tags']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at']

admin.site.register(UserProfile)
admin.site.register(Tag)
