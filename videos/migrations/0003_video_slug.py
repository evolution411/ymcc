# Generated by Django 3.0.1 on 2020-01-19 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20200113_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='slug',
            field=models.SlugField(default='', null=True),
        ),
    ]
