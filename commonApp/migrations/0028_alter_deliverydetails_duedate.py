# Generated by Django 4.2.4 on 2024-01-08 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonApp', '0027_remove_deliverydetails_acceptedqty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverydetails',
            name='dueDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]
