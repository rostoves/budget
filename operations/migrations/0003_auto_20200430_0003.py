# Generated by Django 3.0.5 on 2020-04-29 21:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0002_auto_20200421_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='operation',
            name='import_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
