# Generated by Django 4.2.4 on 2023-12-11 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('quotation_number', models.AutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=255)),
                ('company_name', models.CharField(blank=True, max_length=255)),
                ('contact_person', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(max_length=254)),
                ('billing_address', models.TextField()),
                ('shipping_address', models.TextField(blank=True)),
                ('quotation_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('tax_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('terms_and_conditions', models.TextField(blank=True)),
                ('notes_comments', models.TextField(blank=True)),
                ('sub_total', models.CharField(max_length=255)),
                ('tax_total', models.CharField(max_length=255)),
                ('final_amt', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('trasactionType', models.CharField(blank=True, choices=[('cash', 'Cash'), ('cheque', 'Cheque'), ('neft/rtgs/upi', 'NEFT/RTGS/UPI')], max_length=20, null=True)),
                ('trasactionDetails', models.CharField(blank=True, max_length=20, null=True)),
                ('sale_number', models.AutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=255)),
                ('company_name', models.CharField(blank=True, max_length=255)),
                ('contact_person', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(max_length=254)),
                ('billing_address', models.TextField()),
                ('shipping_address', models.TextField(blank=True)),
                ('sale_date', models.DateField()),
                ('delivery_datesale', models.DateField()),
                ('tax_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('terms_and_conditions', models.TextField(blank=True)),
                ('notes_comments', models.TextField(blank=True)),
                ('advance', models.CharField(blank=True, max_length=255, null=True)),
                ('sub_total', models.CharField(blank=True, max_length=255, null=True)),
                ('tax_total', models.CharField(blank=True, max_length=255, null=True)),
                ('final_amt', models.CharField(blank=True, max_length=255, null=True)),
                ('ledger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.ledger')),
            ],
        ),
        migrations.CreateModel(
            name='ItemRow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_type', models.CharField(choices=[('sales', 'Sales'), ('quotations', 'Quotations')], max_length=20)),
                ('product_name', models.CharField(max_length=255)),
                ('product_description', models.TextField()),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.CharField(max_length=255)),
                ('total_price', models.CharField(max_length=255)),
                ('quotation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sales.quotation')),
                ('sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sales.sales')),
            ],
        ),
    ]
