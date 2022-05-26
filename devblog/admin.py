from django.contrib import admin
from .models import Blog, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):

    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('created_on',)
    summernote_fields = ('content')
    list_display = ('title', 'slug', 'author', 'created_on')
    search_fields = ['title', 'content']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'name', 'content', 'created_on', 'updated_on',)
    list_filter = ('created_on','updated',)
