# Generated by Django 4.2.4 on 2024-01-01 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0011_productionrow_totalcost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionrow',
            name='TotalCost',
            field=models.DecimalField(decimal_places=2, max_digits=50),
        ),
    ]
