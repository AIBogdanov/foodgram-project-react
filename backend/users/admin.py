from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


class CustomUserAdmin(UserAdmin):
    list_filter = ('email', 'username')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscription)
