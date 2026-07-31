from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Team, TeamMember


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Team)
admin.site.register(TeamMember)