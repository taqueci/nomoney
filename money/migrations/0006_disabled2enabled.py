# Generated by Django 3.2.6 on 2022-02-19 15:24

from django.db import migrations, models


def convert_value(apps, schema_editor):
    targets = ('Account', 'Journal', 'Template')

    for m in targets:
        model = apps.get_model('money', m)

        for x in model.objects.all():
            x.enabled = not x.enabled
            x.save()


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0005_auto_20210822_1500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='disabled',
            new_name='enabled',
        ),
        migrations.RenameField(
            model_name='journal',
            old_name='disabled',
            new_name='enabled',
        ),
        migrations.RenameField(
            model_name='template',
            old_name='disabled',
            new_name='enabled',
        ),
        migrations.AlterField(
            model_name='account',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='template',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(convert_value),
    ]
