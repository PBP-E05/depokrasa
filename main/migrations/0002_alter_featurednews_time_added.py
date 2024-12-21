from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='featurednews',
            name='time_added',
            field=models.DateField(default='02/12'),
        ),
    ]
