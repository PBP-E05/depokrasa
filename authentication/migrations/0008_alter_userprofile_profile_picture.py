# Generated by Django 5.1.2 on 2024-10-23 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_remove_userprofile_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pictures/default.jpg', null=True, upload_to='profile_pictures'),
        ),
    ]