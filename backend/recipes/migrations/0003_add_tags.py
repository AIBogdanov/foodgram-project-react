from django.db import migrations
from json import load


with open('data/tags.json', encoding="utf-8") as json_file:
    TAGS = load(json_file)


def add_tag(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    for tag in TAGS:
        new_ingredient = Tag(**tag)
        new_ingredient.save()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_add_ingridiens'),
    ]

    operations = [
        migrations.RunPython(
            add_tag,
        )
    ]
