# Generated by Django 4.2.4 on 2024-01-13 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0013_producedrow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producedrow',
            name='production_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
