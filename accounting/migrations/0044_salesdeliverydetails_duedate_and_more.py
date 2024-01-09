# Generated by Django 4.2.4 on 2024-01-08 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0043_ledgerentry_saleorder_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesdeliverydetails',
            name='dueDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='salesdeliverydetails',
            name='payment',
            field=models.CharField(choices=[('due', 'due'), ('recieved', 'recieved')], default='due', max_length=20),
        ),
    ]
