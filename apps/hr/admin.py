from django.contrib import admin
from .models import Employee, Attendance, Salary

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'user', 'department', 'position', 'employment_status', 'is_active']
    list_filter = ['department', 'employment_status', 'is_active', 'gender']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'email']
    ordering = ['employee_id']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'check_in', 'check_out']
    list_filter = ['status', 'date']
    search_fields = ['employee__employee_id']
    ordering = ['-date']

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['employee', 'month', 'base_salary', 'net_salary', 'paid']
    list_filter = ['paid', 'month']
    search_fields = ['employee__employee_id']
    ordering = ['-month']
