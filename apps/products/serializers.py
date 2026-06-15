from rest_framework import serializers
from apps.core.serializers import BaseSerializer
from .models import Product, Category

class CategorySerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Category
        fields = BaseSerializer.Meta.fields + ['id', 'name', 'description']

class ProductSerializer(BaseSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    margin = serializers.FloatField(read_only=True)
    
    class Meta(BaseSerializer.Meta):
        model = Product
        fields = BaseSerializer.Meta.fields + ['id', 'code', 'name', 'description', 'category', 'category_name', 'unit_price', 'cost_price', 'margin', 'quantity_unit']
