# Generated by Django 2.2.7 on 2019-11-26 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='blogApp',
            new_name='blogs',
        ),
    ]