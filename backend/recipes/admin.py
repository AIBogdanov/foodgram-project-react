from django.contrib.admin import (
    ModelAdmin, StackedInline, register, site
)
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

from .models import AmountIngredient, Ingredient, Recipe, Tag

User = get_user_model()

site.site_header = 'Администрирование Foodgram'
EMPTY_VALUE_DISPLAY = 'Значение не указано'


class IngredientInline(StackedInline):
    model = AmountIngredient
    extra = 2
    min_num = 1


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = (
        'name', 'measurement_unit',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )
    empty_value_display = EMPTY_VALUE_DISPLAY


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = (
        'name', 'author', 'get_image',
        'get_tags',
        'get_is_favorited',
    )
    search_fields = (
        'name', 'author', 'tags'
    )
    list_filter = (
        'name', 'author__username', 'tags'
    )
    inlines = (IngredientInline,)
    empty_value_display = EMPTY_VALUE_DISPLAY
    actions_selection_counter = True

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    def get_tags(self, obj):
        list = []
        for tag in obj.tags.all():
            list.append(tag.name)
        return list

    def get_is_favorited(self, obj):
        count = 0
        for user in User.objects.all():
            if user.favorites.filter(id=obj.id):
                count += 1
        return count

    get_tags.short_description = 'Теги'
    get_image.short_description = 'Изображение'
    get_is_favorited.short_description = 'Число добавлений в избранное'
    


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = (
        'name', 'color', 'slug',
    )
    search_fields = (
        'name', 'color'
    )
    empty_value_display = EMPTY_VALUE_DISPLAY


@register(AmountIngredient)
class AmountIngredientAdmin(ModelAdmin):
    list_display = (
        'recipe', 'ingredients', 'amount',
    )
    search_fields = (
        'recipe', 'ingredients'
    )
