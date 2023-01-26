from django.contrib import admin

from .models import MyUser


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_recipes_count', 'username', 'email',
        'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = (
        'first_name', 'email',
        'is_staff',
    )
    empty_value_display = "Данные отсутствуют"

    def get_recipes_count(self, obj):
        return obj.recipes.count()
    get_recipes_count.short_description = 'Рецептов'


@admin.register(MyUser.subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('username')
