# Generated by Django 4.2.4 on 2023-12-14 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0011_purchasequotation_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasequotation',
            name='supplier',
        ),
        migrations.RemoveField(
            model_name='purchasequotation',
            name='tax_rate',
        ),
        migrations.AddField(
            model_name='purchasequotation',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchasequotation',
            name='csgst_total',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='purchasequotation',
            name='final_amt',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='purchasequotation',
            name='sgst_total',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='purchasequotation',
            name='sub_total',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
