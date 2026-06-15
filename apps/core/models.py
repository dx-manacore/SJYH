from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    """
    Base model with common fields for all models
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='%(class)s_created', verbose_name='أنشأه')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='%(class)s_updated', verbose_name='عدله')
    is_active = models.BooleanField(default=True, verbose_name='نشط')

    class Meta:
        abstract = True
        ordering = ['-created_at']
