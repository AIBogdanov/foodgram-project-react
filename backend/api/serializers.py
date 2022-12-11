from django.db.models import F
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .user_serializer import UserAuthSerializer
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from recipes.validators import validate_zero


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = '__all__',


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(
        write_only=True, validators=[validate_zero]
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')

    # id = serializers.PrimaryKeyRelatedField(read_only=True)
    # name = serializers.ReadOnlyField(source='ingredient.name')
    # amount = serializers.DecimalField(
    #     write_only=True, validators=[validate_zero],
    #     decimal_places=3
    # )
    # measurement_unit = serializers.ReadOnlyField(
    #     source='ingredient.measurement_unit'
    # )

    # class Meta:
    #     model = IngredientRecipe
    #     fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('slug', 'color')


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = UserAuthSerializer(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    ingredients = IngredientRecipeSerializer(
        many=True
    )
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True,
        method_name='is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True,
        method_name='is_in_shopping_cart'
        )

    class Meta:
        exclude = ('favorites', 'shopping_cart')
        model = Recipe

    def add_ingredients(self, recipe, ingredients):
        for ingridient in ingredients:
            IngredientRecipe.objects.bulk_create(
                ingredient_id=ingridient.get('id'),
                amount=ingridient.get('amount'),
                recipe=recipe
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(recipe, ingredients)
        recipe.save()
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        super().update(instance, validated_data)
        instance.ingredients.clear()
        instance.tags.set(tags)
        self.add_ingredients(instance, ingredients)
        instance.save()
        return instance

    def get_ingredients(self, obj):
        obj.ingredients.values(
            'id', 'name', 'measurement_unit',
            amount=F('ingredient_recipe__amount')
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.favorites.filter(pk=obj.pk).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return user.shopping_cart.filter(pk=obj.pk).exists()
        return False


# class RecipeReadSerializer(RecipeWriteSerializer):
#     author = UserAuthSerializer(read_only=True)
#     ingredients = serializers.SerializerMethodField(
#         method_name='ingredients',
#         read_only=True
#     )
#     image = Base64ImageField()
#     tags = TagSerializer(read_only=True, many=True)
#     is_favorited = serializers.SerializerMethodField(
#         read_only=True,
#         method_name='is_favorited'
#     )
#     is_in_shopping_cart = serializers.SerializerMethodField(
#         read_only=True,
#         method_name='is_in_shopping_cart'
#         )

#     def get_ingredients(self, obj):
#         # return IngredientRecipeSerializer(
#         #     IngredientRecipe.objects.filter(recipe=obj).all(),
#         #     many=True
#         # ).data
#         obj.ingredients.values(
#             'id', 'name', 'measurement_unit',
#             amount=F('ingredient_recipe__amount')
#         )

#     def get_is_favorited(self, obj):
#         user = self.context.get('request').user
#         if user.is_authenticated:
#             return user.favorites.filter(pk=obj.pk).exists()
#         return False

#     def get_is_in_shopping_cart(self, obj):
#         user = self.context.get('request').user
#         if user.is_authenticated:
#             return user.shopping_cart.filter(pk=obj.pk).exists()
#         return False

#     class Meta:
#         model = Recipe
#         exclude = ('slug', 'pub_date')
