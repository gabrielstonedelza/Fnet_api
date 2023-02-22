from django.contrib import admin
from .models import User, Profile


# class AdminUsers(admin.ModelAdmin):
#     list_display = ['id', 'username', 'email', 'phone', 'company_name', 'full_name']
#     search_fields = ['id', 'username', 'email', 'phone', 'company_name', 'full_name']
#
#     class Meta:
#         model = User
#
#
# class AdminProfile(admin.ModelAdmin):
#     list_display = ['id', 'user', 'email', 'profile_pic']
#     search_fields = ['id', 'user', 'email', ]
#
#     class Meta:
#         model = Profile


admin.site.register(User)
admin.site.register(Profile)
