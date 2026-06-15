from rest_framework import serializers
from apps.core.serializers import BaseSerializer
from .models import Department

class DepartmentSerializer(BaseSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    
    class Meta(BaseSerializer.Meta):
        model = Department
        fields = BaseSerializer.Meta.fields + ['id', 'name', 'description', 'manager', 'manager_name', 'budget']
