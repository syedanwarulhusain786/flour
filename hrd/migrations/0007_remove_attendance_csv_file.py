# Generated by Django 4.2.4 on 2024-01-09 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrd', '0006_rename_employe_id_employee_employee_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='csv_file',
        ),
    ]