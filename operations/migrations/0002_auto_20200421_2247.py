# Generated by Django 3.0.5 on 2020-04-21 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='owner',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
