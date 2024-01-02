# Generated by Django 4.2.4 on 2023-12-19 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0027_remove_salesdeliverydetails_final_quantity_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesdeliverydetails',
            name='final_quantity_price',
            field=models.CharField(choices=[('pending', 'Pending'), ('delivered', 'Delivered')], default='pending', max_length=20),
        ),
    ]
