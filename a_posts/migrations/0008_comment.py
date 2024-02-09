# Generated by Django 5.0.1 on 2024-02-08 05:29

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_posts', '0007_post_author'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('body', models.CharField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False, unique=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('parent_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='a_posts.post')),
            ],
        ),
    ]