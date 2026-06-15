from rest_framework import serializers
from apps.core.serializers import BaseSerializer
from .models import Employee, Attendance, Salary

class EmployeeSerializer(BaseSerializer):
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta(BaseSerializer.Meta):
        model = Employee
        fields = BaseSerializer.Meta.fields + [
            'id', 'user', 'employee_id', 'full_name', 'phone', 'email',
            'date_of_birth', 'national_id', 'gender', 'department',
            'department_name', 'position', 'salary', 'hire_date',
            'employment_status', 'address', 'emergency_contact', 'emergency_phone'
        ]
        read_only_fields = ['user']

class AttendanceSerializer(BaseSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    
    class Meta(BaseSerializer.Meta):
        model = Attendance
        fields = BaseSerializer.Meta.fields + [
            'id', 'employee', 'employee_name', 'date',
            'status', 'check_in', 'check_out', 'notes'
        ]

class SalarySerializer(BaseSerializer):
    employee_name = serializers.CharField(source='employee.get_full_name', read_only=True)
    net_salary = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    
    class Meta(BaseSerializer.Meta):
        model = Salary
        fields = BaseSerializer.Meta.fields + [
            'id', 'employee', 'employee_name', 'month',
            'base_salary', 'allowances', 'deductions', 'bonus',
            'net_salary', 'paid', 'paid_date', 'notes'
        ]
