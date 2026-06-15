from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class BaseViewSetMixin(viewsets.ModelViewSet):
    """
    Base ViewSet mixin with common functionality
    """
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if hasattr(self, 'filterset_fields'):
            return queryset.filter(is_active=True)
        return queryset
