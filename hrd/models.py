from django.db import models

# Create your models here.



# models.py
from django.db import models

# models.py
from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    joining=models.DateField(auto_now_add=True,null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    position = models.CharField(max_length=50)
    pan_card = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    
    working_days = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
from django.db import models
from .models import Employee
from datetime import datetime, timedelta
# models.py
import csv
from io import TextIOWrapper
from django.db import models
from django.utils import timezone

class Attendance(models.Model):
    ATTENDANCE_CHOICES = [('present', 'Present'), ('absent', 'Absent'),('paid-leave', 'Paid-Leave'),('unpaid-leave', 'Unpaid-Leave')]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=50, choices=ATTENDANCE_CHOICES)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.date}"

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.today().date()

        if self.in_time and self.out_time:
            in_time_dt = datetime.combine(datetime.today(), self.in_time)
            out_time_dt = datetime.combine(datetime.today(), self.out_time)

            # Calculate total hours
            total_hours = (out_time_dt - in_time_dt).seconds / 3600
            self.total_hours = round(total_hours, 2)

        super().save(*args, **kwargs)
    @classmethod
    def import_csv(cls, csv_file):
        csv_reader = csv.DictReader(TextIOWrapper(csv_file.file, encoding='utf-8'))
        for row in csv_reader:
            employee_id = row['employee_id']
            print(employee_id)
            date_ob = row['date']
            in_time_str = row['in_time']
            out_time_str = row['out_time']
            status = row['status']
            date_r = datetime.strptime(date_ob, "%d-%m-%Y")
            date_r = datetime.strptime(date_ob, "%d-%m-%Y").date()

            # Convert time strings to datetime.time
            in_time = datetime.strptime(in_time_str, "%H:%M:%S").time()
            out_time = datetime.strptime(out_time_str, "%H:%M:%S").time()
            # Check if attendance entry with the same emp_id and date already exists
            existing_attendance = cls.objects.filter(employee__id=employee_id, date=date_r).first()

            if existing_attendance:
                # Attendance entry already exists, leave it or handle accordingly
                pass
            else:
                # Create a new attendance entry
                cls.objects.create(
                    employee_id=employee_id,
                    date=date_r,
                    in_time=in_time,
                    out_time=out_time,
                    status=status
                )