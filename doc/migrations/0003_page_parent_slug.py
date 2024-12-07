# Generated by Django 5.1.1 on 2024-10-05 03:59

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    Page = apps.get_model('doc', 'Page')

    for x in Page.objects.exclude(parent=None):
        x.parent_slug = x.parent.slug
        x.save()


def reverse_func(apps, schema_editor):
    Page = apps.get_model('doc', 'Page')

    for x in Page.objects.exlucde(parent_slug=None):
        x.parent = Page.objects.get(slug=x.parent_slug).first()


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0002_page_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='parent_slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.RunPython(forwards_func, reverse_func),
        migrations.RemoveField(
            model_name='page',
            name='parent',
        ),
    ]