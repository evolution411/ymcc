# Generated by Django 3.0.1 on 2020-02-26 02:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogApp', '0008_auto_20200122_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentText', models.TextField()),
                ('commentDate', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('commentPoster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_comment_posters', to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_comments', to='blogApp.Blog')),
            ],
            options={
                'ordering': ['commentDate'],
            },
        ),
    ]