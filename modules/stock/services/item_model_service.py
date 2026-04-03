# Purpose: Business service for ItemModel master data
"""
Item Model Service
Company-scoped CRUD and deactivation logic for item models.
"""
from audit.services.logger import AuditService
from modules.stock.models.brand import Brand
from modules.stock.models.category import StockCategory
from modules.stock.models.item_model import ItemModel
from modules.stock.models.stock_item import StockItem
from modules.stock.models.vendor import Vendor
from modules.stock.services.exceptions import (
    StockConflictError,
    StockDeactivationBlockedError,
    StockValidationError,
)
from modules.stock.services.utils import (
    get_company_entity,
    normalize_code,
    normalize_name,
    snapshot,
)

ENTITY_TYPE = "stock_item_model"

VALID_TRACKING_TYPES = {
    ItemModel.TRACKING_QUANTITY,
    ItemModel.TRACKING_SERIALIZED,
}


class ItemModelService:
    """Business logic for item model management."""

    @staticmethod
    def create_item_model(company, data: dict, actor):
        category_id = data.get("category_id")
        model_name = data.get("model_name")
        tracking_type = data.get("tracking_type")

        if not category_id:
            raise StockValidationError("category_id is required", field="category_id")
        if not model_name:
            raise StockValidationError("model_name is required", field="model_name")
        if not tracking_type:
            raise StockValidationError("tracking_type is required", field="tracking_type")
        if tracking_type not in VALID_TRACKING_TYPES:
            raise StockValidationError(
                f"tracking_type must be one of: {', '.join(sorted(VALID_TRACKING_TYPES))}",
                field="tracking_type",
            )

        normalized_model_name = normalize_name(model_name)
        model_code = data.get("model_code")
        if model_code:
            model_code = normalize_code(model_code)

        # Cross-company FK validation
        category = get_company_entity(
            StockCategory, company, category_id,
            active_only=True, entity_name="stock_category",
        )

        brand = None
        brand_id = data.get("brand_id")
        if brand_id:
            brand = get_company_entity(
                Brand, company, brand_id,
                active_only=True, entity_name="stock_brand",
            )

        vendor_ref = None
        vendor_ref_id = data.get("vendor_reference_id")
        if vendor_ref_id:
            vendor_ref = get_company_entity(
                Vendor, company, vendor_ref_id,
                active_only=True, entity_name="stock_vendor_reference",
            )

        # Duplicate model_code check (DB constraint: is_deleted=False, model_code not null)
        if model_code:
            if ItemModel.objects.filter(
                company=company, model_code=model_code,
                is_deleted=False,
            ).exists():
                raise StockConflictError(
                    f"Item model with code '{model_code}' already exists in this company"
                )

        # Composite identity check (DB constraint: company+category+normalized_model_name+brand, is_deleted=False)
        identity_filter = {
            "company": company,
            "category": category,
            "normalized_model_name": normalized_model_name,
            "brand": brand,
            "is_deleted": False,
        }
        if ItemModel.objects.filter(**identity_filter).exists():
            raise StockConflictError(
                "An item model with the same category, name, and brand already exists in this company"
            )

        item_model = ItemModel.objects.create(
            company=company,
            category=category,
            brand=brand,
            vendor_reference=vendor_ref,
            model_name=model_name.strip(),
            model_code=model_code or None,
            normalized_model_name=normalized_model_name,
            description=data.get("description", ""),
            default_unit=data.get("default_unit", "pcs"),
            tracking_type=tracking_type,
            minimum_stock_level=data.get("minimum_stock_level"),
            image_url=data.get("image_url", ""),
            is_active=True,
            created_by=actor,
            updated_by=actor,
        )

        AuditService.log_event(
            action_code="stock.item_model.created",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(item_model.pk),
            actor_user=actor,
            company=company,
            before_snapshot=None,
            after_snapshot=snapshot(item_model),
        )

        return item_model

    @staticmethod
    def update_item_model(company, model_id, data: dict, actor):
        item_model = get_company_entity(
            ItemModel, company, model_id,
            active_only=True, entity_name=ENTITY_TYPE,
        )
        before = snapshot(item_model)

        # tracking_type is immutable after creation
        if "tracking_type" in data and data["tracking_type"] != item_model.tracking_type:
            raise StockValidationError(
                "tracking_type cannot be changed after creation",
                field="tracking_type",
            )

        if "model_name" in data:
            new_name = data["model_name"].strip()
            new_normalized = normalize_name(data["model_name"])
            item_model.model_name = new_name
            item_model.normalized_model_name = new_normalized

        if "model_code" in data:
            new_code = data["model_code"]
            if new_code:
                new_code = normalize_code(new_code)
                if new_code != item_model.model_code:
                    if ItemModel.objects.filter(
                        company=company, model_code=new_code,
                        is_deleted=False,
                    ).exclude(pk=item_model.pk).exists():
                        raise StockConflictError(
                            f"Item model with code '{new_code}' already exists in this company"
                        )
                item_model.model_code = new_code
            else:
                item_model.model_code = None

        if "category_id" in data:
            category = get_company_entity(
                StockCategory, company, data["category_id"],
                active_only=True, entity_name="stock_category",
            )
            item_model.category = category

        if "brand_id" in data:
            if data["brand_id"] is None:
                item_model.brand = None
            else:
                brand = get_company_entity(
                    Brand, company, data["brand_id"],
                    active_only=True, entity_name="stock_brand",
                )
                item_model.brand = brand

        if "vendor_reference_id" in data:
            if data["vendor_reference_id"] is None:
                item_model.vendor_reference = None
            else:
                vendor_ref = get_company_entity(
                    Vendor, company, data["vendor_reference_id"],
                    active_only=True, entity_name="stock_vendor_reference",
                )
                item_model.vendor_reference = vendor_ref

        for field in ("description", "default_unit", "minimum_stock_level", "image_url"):
            if field in data:
                setattr(item_model, field, data[field])

        # Composite identity check before save (DB constraint: company+category+normalized_model_name+brand, is_deleted=False)
        identity_filter = {
            "company": company,
            "category": item_model.category,
            "normalized_model_name": item_model.normalized_model_name,
            "brand": item_model.brand,
            "is_deleted": False,
        }
        if ItemModel.objects.filter(**identity_filter).exclude(pk=item_model.pk).exists():
            raise StockConflictError(
                "An item model with the same category, name, and brand already exists in this company"
            )

        item_model.updated_by = actor
        item_model.save()

        AuditService.log_event(
            action_code="stock.item_model.updated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(item_model.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(item_model),
        )

        return item_model

    @staticmethod
    def deactivate_item_model(company, model_id, actor):
        item_model = get_company_entity(
            ItemModel, company, model_id,
            active_only=True, entity_name=ENTITY_TYPE,
        )

        stock_count = StockItem.objects.filter(
            company=company, item_model=item_model,
            is_active=True, is_deleted=False,
        ).count()
        if stock_count > 0:
            raise StockDeactivationBlockedError(
                entity_type=ENTITY_TYPE,
                reason=f"{stock_count} active stock items reference this item model",
                blocking_count=stock_count,
            )

        before = snapshot(item_model)
        item_model.is_active = False
        item_model.updated_by = actor
        item_model.save()

        AuditService.log_event(
            action_code="stock.item_model.deactivated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(item_model.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(item_model),
        )

        return item_model
