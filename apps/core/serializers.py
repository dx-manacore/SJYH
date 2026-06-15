from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):
    """
    Base serializer with common fields
    """
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    updated_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ['created_at', 'updated_at', 'created_by', 'updated_by', 'is_active']
