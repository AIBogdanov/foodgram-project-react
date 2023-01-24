from django.contrib import admin

from .models import MyUser


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email',
        'first_name', 'last_name', 'subscribe')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('first_name', 'email')
    empty_value_display = "Данные отсутствуют"
