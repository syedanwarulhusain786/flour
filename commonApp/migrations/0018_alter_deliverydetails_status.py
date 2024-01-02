# Generated by Django 4.2.4 on 2023-12-16 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonApp', '0017_deliverydetails_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverydetails',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('delivered', 'Delivered')], default='pending', max_length=20),
        ),
    ]
