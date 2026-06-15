from django.db import models
from apps.core.models import BaseModel

class Department(BaseModel):
    """
    نموذج القسم
    """
    name = models.CharField(max_length=200, unique=True, verbose_name='اسم القسم')
    description = models.TextField(blank=True, verbose_name='الوصف')
    manager = models.ForeignKey('hr.Employee', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='مدير القسم', related_name='managed_departments')
    budget = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='الميزانية')
    
    class Meta:
        verbose_name = 'قسم'
        verbose_name_plural = 'الأقسام'
        ordering = ['name']

    def __str__(self):
        return self.name
