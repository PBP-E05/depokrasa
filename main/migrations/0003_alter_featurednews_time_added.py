# Generated by Django 5.1.4 on 2024-12-09 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_featurednews_time_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featurednews',
            name='time_added',
            field=models.DateField(default='09/12'),
        ),
    ]