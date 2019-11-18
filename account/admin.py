from django.contrib import admin
from .models import user

@admin.register(user)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'name', 'nickname']
    list_display_links = ['id' , 'email']



