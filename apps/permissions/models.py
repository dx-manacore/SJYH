from django.db import models
from django.contrib.auth.models import User
from apps.core.models import BaseModel

class Role(BaseModel):
    """
    نموذج الأدوار
    """
    ROLE_TYPES = [
        ('admin', 'مسؤول النظام'),
        ('manager', 'مدير'),
        ('accountant', 'محاسب'),
        ('hr_manager', 'مدير الموارد البشرية'),
        ('staff', 'موظف'),
    ]
    
    name = models.CharField(max_length=200, unique=True, verbose_name='اسم الدور')
    role_type = models.CharField(max_length=50, choices=ROLE_TYPES, verbose_name='نوع الدور')
    description = models.TextField(blank=True, verbose_name='الوصف')
    permissions = models.ManyToManyField('Permission', verbose_name='الصلاحيات', related_name='roles')
    
    class Meta:
        verbose_name = 'دور'
        verbose_name_plural = 'الأدوار'
    
    def __str__(self):
        return self.name

class Permission(BaseModel):
    """
    نموذج الصلاحيات
    """
    RESOURCE_TYPES = [
        ('invoices', 'الفواتير'),
        ('inventory', 'المخزون'),
        ('products', 'المنتجات'),
        ('employees', 'الموظفون'),
        ('salaries', 'الرواتب'),
        ('reports', 'التقارير'),
        ('settings', 'الإعدادات'),
    ]
    
    ACTION_TYPES = [
        ('view', 'عرض'),
        ('create', 'إضافة'),
        ('edit', 'تعديل'),
        ('delete', 'حذف'),
        ('export', 'تصدير'),
    ]
    
    name = models.CharField(max_length=200, unique=True, verbose_name='اسم الصلاحية')
    resource = models.CharField(max_length=50, choices=RESOURCE_TYPES, verbose_name='المورد')
    action = models.CharField(max_length=50, choices=ACTION_TYPES, verbose_name='الإجراء')
    description = models.TextField(blank=True, verbose_name='الوصف')
    
    class Meta:
        verbose_name = 'صلاحية'
        verbose_name_plural = 'الصلاحيات'
        unique_together = ['resource', 'action']
    
    def __str__(self):
        return f"{self.get_resource_display()} - {self.get_action_display()}"

class UserRole(BaseModel):
    """
    ربط المستخدمين بالأدوار
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='المستخدم', related_name='user_role')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name='الدور', related_name='user_roles')
    assigned_date = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ التعيين')
    
    class Meta:
        verbose_name = 'دور المستخدم'
        verbose_name_plural = 'أدوار المستخدمين'
        unique_together = ['user', 'role']
    
    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

class AuditLog(BaseModel):
    """
    سجل تدقيق الأنشطة
    """
    ACTION_TYPES = [
        ('create', 'إضافة'),
        ('update', 'تعديل'),
        ('delete', 'حذف'),
        ('view', 'عرض'),
        ('export', 'تصدير'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='المستخدم', related_name='audit_logs')
    action = models.CharField(max_length=50, choices=ACTION_TYPES, verbose_name='الإجراء')
    model_name = models.CharField(max_length=200, verbose_name='نموذج البيانات')
    object_id = models.CharField(max_length=200, verbose_name='معرف الكائن')
    changes = models.JSONField(null=True, blank=True, verbose_name='التغييرات')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='عنوان IP')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='الوقت')
    
    class Meta:
        verbose_name = 'سجل التدقيق'
        verbose_name_plural = 'سجلات التدقيق'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"
