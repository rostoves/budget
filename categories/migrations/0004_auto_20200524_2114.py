# Generated by Django 3.0.5 on 2020-05-24 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_auto_20200421_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchantcode',
            name='category',
            field=models.ForeignKey(default=3, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='category', to='categories.Category'),
        ),
    ]
