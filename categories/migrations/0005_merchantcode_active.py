# Generated by Django 3.0.5 on 2020-05-24 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0004_auto_20200524_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantcode',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
