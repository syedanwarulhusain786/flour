# Generated by Django 4.2.4 on 2024-01-01 11:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0034_purchasequotation_user'),
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='production',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='production',
            name='cutting',
        ),
        migrations.RemoveField(
            model_name='production',
            name='packing',
        ),
        migrations.RemoveField(
            model_name='production',
            name='printing',
        ),
        migrations.RemoveField(
            model_name='production',
            name='ready_to_dispatch',
        ),
        migrations.RemoveField(
            model_name='production',
            name='stitching',
        ),
        migrations.RemoveField(
            model_name='production',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='production',
            name='production_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='production',
            name='sales_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.salesquotation'),
        ),
        migrations.CreateModel(
            name='ProductionRow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('sales_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.salesquotation')),
            ],
        ),
        migrations.AddField(
            model_name='production',
            name='production_rows',
            field=models.ManyToManyField(to='production.productionrow'),
        ),
    ]
