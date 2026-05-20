from django.contrib import admin
from .models import User, Application, Review

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'full_name', 'email', 'phone']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'full_name']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course_name', 'start_date', 'status', 'created_at']
    list_filter = ['status', 'course_name', 'payment_method']
    search_fields = ['user__username', 'user__full_name']
    list_editable = ['status']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'application', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['user__username', 'application__course_name']