# Generated by Django 3.2 on 2022-11-23 19:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import recipes.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(validators=[recipes.validators.validate_zero], verbose_name='Количество')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_recipe', to='recipes.ingredient', verbose_name='Название ингредиента')),
            ],
            options={
                'verbose_name': 'Ингредиент в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецепте',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название тега')),
                ('color', models.CharField(max_length=7, unique=True, validators=[django.core.validators.RegexValidator(message='Неверное значение HEX-кода', regex='^#[a-fA-F\\d]{6}$')], verbose_name='HEX-код цвета')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название рецепта')),
                ('image', models.ImageField(help_text='Добавьте картинку', upload_to='recipes/', verbose_name='Фото блюда')),
                ('text', models.TextField(help_text='Введите описание рецепта', verbose_name='Описание рецепта')),
                ('cooking_time', models.PositiveSmallIntegerField(help_text='Время в минутах', validators=[recipes.validators.validate_zero], verbose_name='Время приготовления в минутах')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
                ('favorites', models.ManyToManyField(blank=True, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Избранное')),
                ('ingredients', models.ManyToManyField(related_name='ingredients', through='recipes.IngredientRecipe', to='recipes.Ingredient', verbose_name='Ингредиенты')),
                ('shopping_cart', models.ManyToManyField(blank=True, related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='Список покупок')),
                ('tags', models.ManyToManyField(related_name='tags', to='recipes.Tag', verbose_name='Тэги')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-id'],
            },
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
