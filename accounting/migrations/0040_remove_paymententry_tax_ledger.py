# Generated by Django 4.2.4 on 2024-01-08 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0039_paymententry_comment_paymententry_from_ledger_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymententry',
            name='tax_ledger',
        ),
    ]
