# Generated by Django 4.2.16 on 2024-12-22 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_featurednews_time_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featurednews',
            name='time_added',
            field=models.DateField(default='22/12'),
        ),
    ]
