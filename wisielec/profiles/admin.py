from django.contrib import admin
from models import UserProfile, Achievement


class UserAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ["username", "is_active", "is_superuser", "is_staff", "email", "score", "date_joined", "last_login", ]


class AchievementAdmin(admin.ModelAdmin):
    model = Achievement
    list_display = ["name", "description", "expression", ]

admin.site.register(UserProfile, UserAdmin)
admin.site.register(Achievement, AchievementAdmin)
