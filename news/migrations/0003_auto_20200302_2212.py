# Generated by Django 3.0.1 on 2020-03-03 03:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_headline_newsdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='headline',
            name='newsdate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]