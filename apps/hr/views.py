from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.core.mixins import BaseViewSetMixin
from .models import Employee, Attendance, Salary
from .serializers import EmployeeSerializer, AttendanceSerializer, SalarySerializer

class EmployeeViewSet(BaseViewSetMixin):
    queryset = Employee.objects.select_related('user', 'department')
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'employment_status', 'is_active']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'email']
    ordering_fields = ['employee_id', 'hire_date', 'salary']

class AttendanceViewSet(BaseViewSetMixin):
    queryset = Attendance.objects.select_related('employee')
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'status', 'date']
    search_fields = ['employee__employee_id', 'employee__user__first_name']
    ordering_fields = ['-date', 'employee']

class SalaryViewSet(BaseViewSetMixin):
    queryset = Salary.objects.select_related('employee')
    serializer_class = SalarySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'paid', 'month']
    search_fields = ['employee__employee_id', 'employee__user__first_name']
    ordering_fields = ['-month', 'employee']
