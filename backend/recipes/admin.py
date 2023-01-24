from django.contrib.admin import ModelAdmin, StackedInline, register, site
from django.utils.safestring import mark_safe

from .models import AmountIngredient, Ingredient, Recipe, Tag

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
    )
    fields = (
        ('is_favorited_count'),
        ('name', 'cooking_time',),
        ('author', 'tags',),
        ('text',),
        ('image',),
    )
    # raw_id_fields = ('author', )
    search_fields = (
        'name', 'author', 'tags'
    )
    list_filter = (
        'name', 'author__username', 'tags'
    )

    inlines = (IngredientInline,)
    empty_value_display = EMPTY_VALUE_DISPLAY

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    get_image.short_description = 'Изображение'


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = (
        'name', 'color', 'slug',
    )
    search_fields = (
        'name', 'color'
    )
    empty_value_display = EMPTY_VALUE_DISPLAY
