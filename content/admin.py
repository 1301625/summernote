from django.contrib import admin
from .models import Post
from .forms import PostForm

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    form = PostForm
    summernote_fields = ('content',)
    list_display = ['title', 'content', 'user_count', 'user_max_count', 'deadline','author']
