# Generated by Django 4.2.4 on 2024-01-14 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_alter_accounttype_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billing_company',
            name='industry',
        ),
        migrations.RemoveField(
            model_name='billing_company',
            name='logo',
        ),
    ]