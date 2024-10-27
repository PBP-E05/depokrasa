# Generated by Django 5.1.2 on 2024-10-26 04:32

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeaturedNews',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('icon_image', models.ImageField(blank=True, null=True, upload_to='featured_news')),
                ('grand_title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=255)),
                ('grand_image', models.ImageField(blank=True, null=True, upload_to='featured_news')),
                ('cooking_time', models.IntegerField()),
                ('calories', models.IntegerField()),
                ('comments', models.IntegerField(default=113)),
                ('time_added', models.DateField(default='26/10')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),

        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]