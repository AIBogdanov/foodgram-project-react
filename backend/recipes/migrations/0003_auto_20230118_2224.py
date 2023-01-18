from django.db import migrations
from json import load


with open('data/tags.json', encoding="utf-8") as json_file:
    TAGS = load(json_file)


def add_tag(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    for tag in TAGS:
        new_tag = Tag(**tag)
        new_tag.save()


class Migration(migrations.Migration):
    dependencies = [
        ('recipes', '0002_auto_20230118_2223'),
    ]
    operations = [
        migrations.RunPython(
            add_tag,
        )
    ]
