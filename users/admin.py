from django.contrib import admin
from .models import User, Profile


class AdminUsers(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone', 'company_name', 'full_name']
    search_fields = ['id', 'username', 'email', 'phone', 'company_name', 'full_name']

    class Meta:
        model = User


admin.site.register(User, AdminUsers)
admin.site.register(Profile)
