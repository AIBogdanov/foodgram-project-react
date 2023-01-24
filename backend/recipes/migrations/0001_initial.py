from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AmountIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1, 'Нужно хоть какое-то количество.'), django.core.validators.MaxValueValidator(10000, 'Слишком много!')], verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'Количество ингредиентов',
                'ordering': ('recipe',),
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='ингредиент')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'ингредиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название блюда')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение блюда')),
                ('text', models.TextField(max_length=5000, verbose_name='Описание блюда')),
                ('cooking_time', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1, 'Ваше блюдо уже готово!'), django.core.validators.MaxValueValidator(600, 'Очень долго ждать...')], verbose_name='Время приготовления')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Тэг')),
                ('color', models.CharField(blank=True, default='FF', max_length=7, null=True, verbose_name='Цветовой HEX-код')),
                ('slug', models.CharField(max_length=200, unique=True, verbose_name='Слаг тэга')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'ordering': ('name',),
            },
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.CheckConstraint(check=models.Q(('name__length__gt', 0)), name='\nrecipes_tag_name is empty\n'),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.CheckConstraint(check=models.Q(('color__length__gt', 0)), name='\nrecipes_tag_color is empty\n'),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.CheckConstraint(check=models.Q(('slug__length__gt', 0)), name='\nrecipes_tag_slug is empty\n'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='cart',
            field=models.ManyToManyField(related_name='carts', to=settings.AUTH_USER_MODEL, verbose_name='Список покупок'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='favorite',
            field=models.ManyToManyField(related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Понравившиеся рецепты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.AmountIngredient', to='recipes.Ingredient', verbose_name='Ингредиенты блюда'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='Тег'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_for_ingredient'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.CheckConstraint(check=models.Q(('name__length__gt', 0)), name='\nrecipes_ingredient_name is empty\n'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.CheckConstraint(check=models.Q(('measurement_unit__length__gt', 0)), name='\nrecipes_ingredient_measurement_unit is empty\n'),
        ),
        migrations.AddField(
            model_name='amountingredient',
            name='ingredients',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to='recipes.ingredient', verbose_name='Связанные ингредиенты'),
        ),
        migrations.AddField(
            model_name='amountingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.recipe', verbose_name='В каких рецептах'),
        ),
        migrations.AddConstraint(
            model_name='recipe',
            constraint=models.UniqueConstraint(fields=('name', 'author'), name='unique_for_author'),
        ),
        migrations.AddConstraint(
            model_name='recipe',
            constraint=models.CheckConstraint(check=models.Q(('name__length__gt', 0)), name='\nrecipes_recipe_name is empty\n'),
        ),
        migrations.AddConstraint(
            model_name='amountingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredients'), name='\nrecipes_amountingredient ingredient alredy added\n'),
        ),
    ]
