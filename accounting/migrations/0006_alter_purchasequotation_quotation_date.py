# Generated by Django 4.2.4 on 2023-12-12 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0005_tax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchasequotation',
            name='quotation_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
