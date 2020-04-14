# Generated by Django 3.0.4 on 2020-04-14 03:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('money', '0002_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='journal',
            name='credit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='journal_credit', to='money.Account'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='debit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='journal_debit', to='money.Account'),
        ),
        migrations.AlterField(
            model_name='template',
            name='credit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='template_credit', to='money.Account'),
        ),
        migrations.AlterField(
            model_name='template',
            name='debit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='template_debit', to='money.Account'),
        ),
    ]
