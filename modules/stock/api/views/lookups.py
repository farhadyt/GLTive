# Purpose: Lightweight read-only ViewSets for UI dropdown lookups
"""
Lookup Views
Minimal read-only endpoints for UI dropdowns. Company-scoped, active-only.
"""
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from core.api.base import CompanyResolveMixin
from core.permissions.base import IsCompanyMember
from modules.stock.api.permissions import CanViewStock
from modules.stock.api.serializers.lookups import (
    CategoryLookupSerializer,
    BrandLookupSerializer,
    VendorLookupSerializer,
    WarehouseLookupSerializer,
    ItemModelLookupSerializer,
    StockItemLookupSerializer,
)
from modules.stock.models import (
    StockCategory,
    Brand,
    Vendor,
    Warehouse,
    ItemModel,
    StockItem,
)


class _BaseLookupViewSet(CompanyResolveMixin, ListModelMixin, GenericViewSet):
    """Base lookup viewset with common configuration."""
    permission_classes = [IsAuthenticated, IsCompanyMember, CanViewStock]
    pagination_class = None

    def get_queryset(self):
        if not hasattr(self.request, "company") or self.request.company is None:
            return self.queryset.none()
        return self.queryset.filter(
            company=self.request.company, is_active=True, is_deleted=False,
        )


class CategoryLookupViewSet(_BaseLookupViewSet):
    queryset = StockCategory.objects.all()
    serializer_class = CategoryLookupSerializer


class BrandLookupViewSet(_BaseLookupViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandLookupSerializer


class VendorLookupViewSet(_BaseLookupViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorLookupSerializer


class WarehouseLookupViewSet(_BaseLookupViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseLookupSerializer


class ItemModelLookupViewSet(_BaseLookupViewSet):
    queryset = ItemModel.objects.all()
    serializer_class = ItemModelLookupSerializer


class StockItemLookupViewSet(_BaseLookupViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemLookupSerializer
