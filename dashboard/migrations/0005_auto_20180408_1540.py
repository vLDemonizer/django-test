# Generated by Django 2.0.4 on 2018-04-08 15:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_auto_20180408_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=None, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='cod',
            field=models.CharField(default='0', max_length=32, unique=True),
        ),
    ]
