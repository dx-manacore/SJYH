from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import BaseModel

class Category(BaseModel):
    """
    فئة المنتجات
    """
    name = models.CharField(max_length=200, unique=True, verbose_name='اسم الفئة')
    description = models.TextField(blank=True, verbose_name='الوصف')
    
    class Meta:
        verbose_name = 'فئة منتج'
        verbose_name_plural = 'فئات المنتجات'
    
    def __str__(self):
        return self.name

class Product(BaseModel):
    """
    نموذج المنتج
    """
    code = models.CharField(max_length=100, unique=True, verbose_name='رمز المنتج')
    name = models.CharField(max_length=200, verbose_name='اسم المنتج')
    description = models.TextField(blank=True, verbose_name='الوصف')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='الفئة', related_name='products')
    unit_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='سعر الوحدة')
    cost_price = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='سعر التكلفة')
    quantity_unit = models.CharField(max_length=50, default='قطعة', verbose_name='وحدة القياس')
    
    class Meta:
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    @property
    def margin(self):
        """
        حساب الهامش
        """
        if self.cost_price == 0:
            return 0
        return ((self.unit_price - self.cost_price) / self.cost_price) * 100
