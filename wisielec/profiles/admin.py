from django.contrib import admin
from models import UserProfile

class UserAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ["username", "is_active", "is_superuser", "is_staff", "email", "score", "date_joined", "last_login", ]

admin.site.register(UserProfile, UserAdmin)