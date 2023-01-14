# from django.contrib.admin import register
# from django.contrib.auth.admin import UserAdmin

# from .models import MyUser


# @register(MyUser)
# class MyUserAdmin(UserAdmin):
#     list_display = (
#         'username', 'first_name', 'last_name', 'email',
#     )
#     fields = (
#         ('username', 'email', ),
#         ('first_name', 'last_name', ),
#     )
#     fieldsets = []

#     search_fields = (
#         'username', 'email',
#     )
#     list_filter = (
#         'first_name', 'email',
#     )
#     save_on_top = True
from django.contrib import admin

from .models import MyUser

@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email',
        'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('first_name', 'email')
    empty_value_display = "Данные отсутствуют"
