from django.contrib import admin
from .models import Post
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content', 'timestamp')
    search_fields = ('content', 'author__username')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'last_login')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('username',)
