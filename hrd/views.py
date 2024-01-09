from django.shortcuts import render

# Create your views here.
# views.py
import csv
from django.http import HttpResponse
from .models import Attendance
# views.py
from django.shortcuts import render
from .models import Employee, Attendance
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from .forms import EmployeeForm


def calculate_salary(employee_id):
    employee = Employee.objects.get(pk=employee_id)
    total_hours_worked = Attendance.objects.filter(employee=employee).aggregate(total_hours=models.Sum('hours_worked'))['total_hours']
    salary = employee.salary * (total_hours_worked / 160)  # Assuming 160 hours in a month
    return salary

def hr_department(request):
    employees=Employee.objects.all()

    return render(request, 'employee/employee_list.html',{'employees':employees})

def import_attendance(request):
    with open('attendance.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            employee_id, date, hours_worked = row
            Attendance.objects.create(
                employee_id=employee_id,
                date=date,
                hours_worked=hours_worked
            )

    return HttpResponse('Attendance imported successfully!')
# views.py
from django.shortcuts import render, redirect
from .forms import EmployeeForm

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hr_department')  # Assuming you have a URL pattern named 'employee_list'
    else:
        form = EmployeeForm()

    return render(request, 'employee/add_employee.html', {'form': form})

def employee_edit(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('hr_department')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'employee/add_employee.html', {'form': form, 'employee': employee})

def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    if request.method == 'POST':
        employee.delete()
        return redirect('hr_department')  # Change this to the URL name of your employee list view

    return render(request, 'employee/employee_delete.html', {'employee': employee})


from .models import Attendance
from .forms import AttendanceForm
from datetime import datetime, timedelta




def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('month_wise_attendance')
    else:
        form = AttendanceForm()

    return render(request, 'attendence/mark_attendence.html', {'form': form})

# views.py
from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from .models import Attendance
from .forms import AttendanceForm
from calendar import monthrange
# views.py
from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime, timedelta
from calendar import monthrange
from .models import Attendance
# views.py
from django.shortcuts import render
from datetime import datetime, timedelta
from calendar import monthrange
from .models import Attendance

# views.py
from django.shortcuts import render
from datetime import datetime, timedelta
from calendar import monthrange
from .models import Attendance



from .forms import UploadAttendanceForm
from .models import Attendance

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Attendance

def upload_attendance_page(request):
    if request.method == 'POST':
        form = UploadAttendanceForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            # try:
            Attendance.import_csv(csv_file)
            return redirect('upload_attendance_page')  # Redirect to the same page after successful upload
            # except Exception as e:
            #     error_message = f'Error importing attendance data: {str(e)}'
    else:
        form = UploadAttendanceForm()
        error_message = None

    return render(request, 'attendence/upload_attendance.html', {'form': form, 'error_message': error_message})










def month_wise_attendance(request):
        # Get the selected year and month from the request parameters
    year = int(request.GET.get('year', datetime.today().year))
    month = int(request.GET.get('month', datetime.today().month))


    if year is None or month is None:
        today = datetime.today()
        year = today.year
        month = today.month
        # Generate a list of tuples containing month number and month name
    months = [(i, datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)]

    # Generate a list of years (you can customize the range as needed)
    years = range(datetime.today().year - 5, datetime.today().year + 6)
    first_day = datetime(year, month, 1).date()
    last_day = datetime(year, month, monthrange(year, month)[1]).date()

    all_dates = [first_day + timedelta(days=x) for x in range((last_day - first_day).days + 1)]
    emps = Employee.objects.all()
    attendance_data=[]
    for record in emps:
        attendance_records = Attendance.objects.filter(date__range=(first_day, last_day)).order_by('employee_id')
        user_data = {
                        'employee_id': record.employee_id,
                        'user': f"{record.first_name} {record.last_name}",
                        'attendance': {},
                    }
            

        for date in all_dates:
            try:
                attendance_record = Attendance.objects.get(employee=record, date=date)
                user_data['attendance'][date] = {
                'status': attendance_record.status ,
            }
            except Exception as e:
                user_data['attendance'][date] = {
                'status': 'N/A' ,
            }
        
            

        attendance_data.append(user_data)

    context = {
        'months':months,
        'years':years,
        'year': year,
        'month': month,
        'all_dates': all_dates,
        'attendance_data': attendance_data,
    }




    return render(request, 'attendence/month_wise_attendance.html', context)
# views.p/y
from django.shortcuts import render, redirect
from .forms import AttendanceForm

def upload_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')  # Replace 'attendance_list' with your actual URL name
    else:
        form = AttendanceForm()

    return render(request, 'attendence/upload_attendance.html', {'form': form})


