# Generated by Django 5.1.3 on 2024-12-02 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0008_attachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='tags',
            field=models.ManyToManyField(blank=True, to='money.tag'),
        ),
    ]