# Generated by Django 2.0.4 on 2018-04-08 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20180408_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='total_local',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='total_usd',
            field=models.FloatField(),
        ),
    ]
