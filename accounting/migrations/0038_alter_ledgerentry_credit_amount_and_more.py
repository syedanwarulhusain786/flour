# Generated by Django 4.2.4 on 2024-01-08 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0037_alter_ledgerentry_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ledgerentry',
            name='credit_amount',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
        migrations.AlterField(
            model_name='ledgerentry',
            name='debit_amount',
            field=models.DecimalField(decimal_places=2, max_digits=100),
        ),
    ]