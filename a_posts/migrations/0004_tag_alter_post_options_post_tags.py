# Generated by Django 5.0.1 on 2024-01-30 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_posts', '0003_alter_post_options_rename_created_at_post_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('slug', models.SlugField(max_length=20, unique=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='a_posts.tag'),
        ),
    ]
