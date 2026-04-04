# Purpose: CRUD ViewSets for stock master data entities
"""
Master Data ViewSets
Service-layer pattern: create/update/partial_update override — NOT perform_create/perform_update.
"""
from rest_framework.decorators import action

from core.api.base import CompanyScopedViewSet
from modules.stock.api.permissions import CanManageMasterData, CanViewStock
from modules.stock.api.serializers.master_data import (
    CategorySerializer,
    BrandSerializer,
    VendorSerializer,
    ItemModelCreateSerializer,
    ItemModelUpdateSerializer,
    ItemModelOutputSerializer,
    WarehouseSerializer,
)
from modules.stock.models import (
    StockCategory,
    Brand,
    Vendor,
    ItemModel,
    Warehouse,
)
from modules.stock.services import (
    CategoryService,
    BrandService,
    VendorService,
    ItemModelService,
    WarehouseService,
)
from shared.responses.base import success_response, created_response


class CategoryViewSet(CompanyScopedViewSet):
    queryset = StockCategory.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            is_active=True, is_deleted=False,
        ).order_by("sort_order", "name")

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [CanViewStock()]
        return [CanManageMasterData()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = CategoryService.create_category(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return created_response(data=output.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=kwargs.get("partial", False))
        serializer.is_valid(raise_exception=True)
        result = CategoryService.update_category(
            company=request.company,
            category_id=instance.pk,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return success_response(data=output.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        instance = self.get_object()
        result = CategoryService.deactivate_category(
            company=request.company,
            category_id=instance.pk,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return success_response(data=output.data)


class BrandViewSet(CompanyScopedViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            is_active=True, is_deleted=False,
        ).order_by("name")

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [CanViewStock()]
        return [CanManageMasterData()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = BrandService.create_brand(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return created_response(data=output.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=kwargs.get("partial", False))
        serializer.is_valid(raise_exception=True)
        result = BrandService.update_brand(
            company=request.company,
            brand_id=instance.pk,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return success_response(data=output.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        instance = self.get_object()
        result = BrandService.deactivate_brand(
            company=request.company,
            brand_id=instance.pk,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return success_response(data=output.data)


class VendorViewSet(CompanyScopedViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            is_active=True, is_deleted=False,
        ).order_by("name")

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [CanViewStock()]
        return [CanManageMasterData()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = VendorService.create_vendor(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return created_response(data=output.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=kwargs.get("partial", False))
        serializer.is_valid(raise_exception=True)
        result = VendorService.update_vendor(
            company=request.company,
            vendor_id=instance.pk,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return success_response(data=output.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        instance = self.get_object()
        result = VendorService.deactivate_vendor(
            company=request.company,
            vendor_id=instance.pk,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return success_response(data=output.data)


class ItemModelViewSet(CompanyScopedViewSet):
    queryset = ItemModel.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(
            is_active=True, is_deleted=False,
        ).order_by("model_name")

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [CanViewStock()]
        return [CanManageMasterData()]

    def get_serializer_class(self):
        if self.action == "create":
            return ItemModelCreateSerializer
        if self.action in ("update", "partial_update"):
            return ItemModelUpdateSerializer
        return ItemModelOutputSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = ItemModelService.create_item_model(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = ItemModelOutputSerializer(result)
        return created_response(data=output.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=kwargs.get("partial", False))
        serializer.is_valid(raise_exception=True)
        result = ItemModelService.update_item_model(
            company=request.company,
            model_id=instance.pk,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = ItemModelOutputSerializer(result)
        return success_response(data=output.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        instance = self.get_object()
        result = ItemModelService.deactivate_item_model(
            company=request.company,
            model_id=instance.pk,
            actor=request.user,
        )
        output = ItemModelOutputSerializer(result)
        return success_response(data=output.data)


class WarehouseViewSet(CompanyScopedViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            is_active=True, is_deleted=False,
        ).order_by("code")

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [CanViewStock()]
        return [CanManageMasterData()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = WarehouseService.create_warehouse(
            company=request.company,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return created_response(data=output.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=kwargs.get("partial", False))
        serializer.is_valid(raise_exception=True)
        result = WarehouseService.update_warehouse(
            company=request.company,
            warehouse_id=instance.pk,
            data=serializer.validated_data,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return success_response(data=output.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        instance = self.get_object()
        result = WarehouseService.deactivate_warehouse(
            company=request.company,
            warehouse_id=instance.pk,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return success_response(data=output.data)

    @action(detail=True, methods=["post"], url_path="set-default")
    def set_default(self, request, pk=None):
        instance = self.get_object()
        result = WarehouseService.set_default_warehouse(
            company=request.company,
            warehouse_id=instance.pk,
            actor=request.user,
        )
        output = self.get_serializer(result)
        return success_response(data=output.data)
