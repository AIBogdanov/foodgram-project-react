from django.db import migrations
from json import load


with open('data/ingredients.json', encoding="utf-8") as json_file:
    INGREDIENTS = load(json_file)


def add_ingredient(apps, schema_editor):
    Ingredient = apps.get_model('recipes', 'Ingredient')
    for ingredient in INGREDIENTS:
        new_ingredient = Ingredient(
            name=ingredient['name'],
            measurement_unit=ingredient['measurement_unit']
        )
        new_ingredient.save()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_ingredient,
        )
    ]
