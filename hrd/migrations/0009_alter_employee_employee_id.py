# Generated by Django 4.2.4 on 2024-01-09 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrd', '0008_attendance_in_time_attendance_out_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='employee_id',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]