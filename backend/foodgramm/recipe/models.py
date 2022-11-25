from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredients(models.Model):
    """Модель ингрединтов, создаются только администратором."""
    name = models.CharField(max_length=50)
    measurement_unit = models.CharField(max_length=10)

    class Meta:
        ordering = ('-id',)
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit')
            ),
        )

    def __str__(self):
        return self.name


class NumberIngredient(models.Model):
    """Связанная модель ингредиент и его количество для рецепта."""
    Ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='numberingredient')
    number = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель для тегов. С разными цветами."""
    name = models.CharField(
        max_length=20,
        unique=True,
        help_text='Введите название тега.',
    )
    color = models.CharField(max_length=7)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe')
    name = models.CharField(max_length=200)
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )
    description = models.TextField()
    ingredient = models.ManyToManyField(
        NumberIngredient,
        related_name='recipe'
    )
    tag = models.ManyToManyField(
        Tag,
        related_name='recipe'
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favourite(models.Model):
    """Модель для любимых рецептов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourite')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourite')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            )
        ]

    def __str__(self):
        return self.name


class ShoopingList(models.Model):
    """Модель для списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourite')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourite')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite'
            )
        ]

    def __str__(self):
        return self.name
