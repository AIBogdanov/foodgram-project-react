from django.db import migrations
import json


with open('./data/ingredients.json', encoding="utf-8") as json_file:
    INGREDIENTS = json.load(json_file)


def add_ingridient(apps, schema_editor):
    Ingridient = apps.get_model('recipes', 'Ingredient')
    for ingredient in INGREDIENTS:
        new_ingredient = Ingridient(
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
            add_ingridient,
        )
    ]
