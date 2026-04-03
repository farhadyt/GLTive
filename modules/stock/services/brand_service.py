# Purpose: Business service for Brand master data
"""
Brand Service
Company-scoped CRUD and deactivation logic for brands.
"""
from audit.services.logger import AuditService
from modules.stock.models.brand import Brand
from modules.stock.models.item_model import ItemModel
from modules.stock.services.exceptions import (
    StockConflictError,
    StockDeactivationBlockedError,
    StockValidationError,
)
from modules.stock.services.utils import (
    get_company_entity,
    normalize_name,
    snapshot,
)

ENTITY_TYPE = "stock_brand"


class BrandService:
    """Business logic for brand management."""

    @staticmethod
    def create_brand(company, data: dict, actor):
        name = data.get("name")
        if not name:
            raise StockValidationError("name is required", field="name")

        normalized = normalize_name(name)

        if Brand.objects.filter(
            company=company, normalized_name=normalized,
            is_active=True, is_deleted=False,
        ).exists():
            raise StockConflictError(
                f"Active brand with name '{name.strip()}' already exists in this company"
            )

        brand = Brand.objects.create(
            company=company,
            name=name.strip(),
            normalized_name=normalized,
            description=data.get("description", ""),
            website=data.get("website", ""),
            is_active=True,
            created_by=actor,
            updated_by=actor,
        )

        AuditService.log_event(
            action_code="stock.brand.created",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(brand.pk),
            actor_user=actor,
            company=company,
            before_snapshot=None,
            after_snapshot=snapshot(brand),
        )

        return brand

    @staticmethod
    def update_brand(company, brand_id, data: dict, actor):
        brand = get_company_entity(
            Brand, company, brand_id,
            active_only=True, entity_name=ENTITY_TYPE,
        )
        before = snapshot(brand)

        if "name" in data:
            new_name = data["name"].strip()
            new_normalized = normalize_name(data["name"])
            if new_normalized != brand.normalized_name:
                if Brand.objects.filter(
                    company=company, normalized_name=new_normalized,
                    is_active=True, is_deleted=False,
                ).exclude(pk=brand.pk).exists():
                    raise StockConflictError(
                        f"Active brand with name '{new_name}' already exists in this company"
                    )
                brand.normalized_name = new_normalized
            brand.name = new_name

        if "description" in data:
            brand.description = data["description"]

        if "website" in data:
            brand.website = data["website"]

        brand.updated_by = actor
        brand.save()

        AuditService.log_event(
            action_code="stock.brand.updated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(brand.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(brand),
        )

        return brand

    @staticmethod
    def deactivate_brand(company, brand_id, actor):
        brand = get_company_entity(
            Brand, company, brand_id,
            active_only=True, entity_name=ENTITY_TYPE,
        )

        model_count = ItemModel.objects.filter(
            company=company, brand=brand,
            is_active=True, is_deleted=False,
        ).count()
        if model_count > 0:
            raise StockDeactivationBlockedError(
                entity_type=ENTITY_TYPE,
                reason=f"{model_count} active item models reference this brand",
                blocking_count=model_count,
            )

        before = snapshot(brand)
        brand.is_active = False
        brand.updated_by = actor
        brand.save()

        AuditService.log_event(
            action_code="stock.brand.deactivated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(brand.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(brand),
        )

        return brand
