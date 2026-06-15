from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import BaseModel

class Employee(BaseModel):
    """
    نموذج الموظف
    """
    EMPLOYMENT_STATUS_CHOICES = [
        ('active', 'نشط'),
        ('inactive', 'غير نشط'),
        ('leave', 'إجازة'),
        ('terminated', 'منتهية العقد'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'ذكر'),
        ('female', 'أنثى'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='المستخدم')
    employee_id = models.CharField(max_length=50, unique=True, verbose_name='رقم الموظف')
    phone = models.CharField(max_length=20, verbose_name='رقم الهاتف')
    email = models.EmailField(verbose_name='البريد الإلكتروني')
    date_of_birth = models.DateField(verbose_name='تاريخ الميلاد')
    national_id = models.CharField(max_length=20, unique=True, verbose_name='الهوية الوطنية')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='الجنس')
    department = models.ForeignKey('departments.Department', on_delete=models.SET_NULL, null=True, verbose_name='القسم', related_name='employees')
    position = models.CharField(max_length=200, verbose_name='المسمى الوظيفي')
    salary = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='الراتب الأساسي')
    hire_date = models.DateField(verbose_name='تاريخ التعيين')
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, default='active', verbose_name='حالة التوظيف')
    address = models.TextField(verbose_name='العنوان')
    emergency_contact = models.CharField(max_length=200, verbose_name='جهة الاتصال في حالات الطوارئ')
    emergency_phone = models.CharField(max_length=20, verbose_name='رقم هاتف الطوارئ')
    
    class Meta:
        verbose_name = 'موظف'
        verbose_name_plural = 'الموظفون'
        ordering = ['employee_id']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"
    
    def get_full_name(self):
        return self.user.get_full_name()

class Attendance(BaseModel):
    """
    نموذج الحضور والغياب
    """
    STATUS_CHOICES = [
        ('present', 'حاضر'),
        ('absent', 'غائب'),
        ('late', 'متأخر'),
        ('leave', 'إجازة'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='الموظف', related_name='attendances')
    date = models.DateField(verbose_name='التاريخ')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='الحالة')
    check_in = models.TimeField(null=True, blank=True, verbose_name='وقت الحضور')
    check_out = models.TimeField(null=True, blank=True, verbose_name='وقت المغادرة')
    notes = models.TextField(blank=True, verbose_name='ملاحظات')
    
    class Meta:
        verbose_name = 'حضور'
        verbose_name_plural = 'الحضور والغياب'
        unique_together = ['employee', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.get_status_display()}"

class Salary(BaseModel):
    """
    نموذج الراتب والمكافآت
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='الموظف', related_name='salaries')
    month = models.DateField(verbose_name='الشهر')
    base_salary = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='الراتب الأساسي')
    allowances = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='البدلات')
    deductions = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='الخصومات')
    bonus = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='المكافأة')
    net_salary = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='الراتب الصافي')
    paid = models.BooleanField(default=False, verbose_name='مدفوع')
    paid_date = models.DateField(null=True, blank=True, verbose_name='تاريخ الصرف')
    notes = models.TextField(blank=True, verbose_name='ملاحظات')
    
    class Meta:
        verbose_name = 'الراتب'
        verbose_name_plural = 'الرواتب'
        unique_together = ['employee', 'month']
        ordering = ['-month']
    
    def __str__(self):
        return f"{self.employee.employee_id} - {self.month}"
    
    def calculate_net_salary(self):
        total = self.base_salary + self.allowances + self.bonus - self.deductions
        return max(0, total)
