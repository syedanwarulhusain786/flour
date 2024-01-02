# Generated by Django 4.2.4 on 2024-01-02 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commonApp', '0021_productstock_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productstock',
            name='type',
            field=models.CharField(choices=[('purchase', 'Purchase'), ('return', 'Return'), ('prod', 'Prod')], default='purchase', max_length=10),
        ),
    ]