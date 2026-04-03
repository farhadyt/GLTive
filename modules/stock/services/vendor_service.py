# Purpose: Business service for Vendor master data
"""
Vendor Service
Company-scoped CRUD and deactivation logic for vendors.
"""
from audit.services.logger import AuditService
from modules.stock.models.vendor import Vendor
from modules.stock.models.item_model import ItemModel
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

ENTITY_TYPE = "stock_vendor_reference"


class VendorService:
    """Business logic for vendor management."""

    @staticmethod
    def create_vendor(company, data: dict, actor):
        name = data.get("name")
        if not name:
            raise StockValidationError("name is required", field="name")

        normalized = normalize_name(name)

        if Vendor.objects.filter(
            company=company, normalized_name=normalized,
            is_active=True, is_deleted=False,
        ).exists():
            raise StockConflictError(
                f"Active vendor with name '{name.strip()}' already exists in this company"
            )

        code = data.get("code")
        if code:
            code = normalize_code(code)
            if Vendor.objects.filter(
                company=company, code=code,
                is_active=True, is_deleted=False,
            ).exists():
                raise StockConflictError(
                    f"Active vendor with code '{code}' already exists in this company"
                )

        vendor = Vendor.objects.create(
            company=company,
            name=name.strip(),
            normalized_name=normalized,
            code=code or None,
            contact_person=data.get("contact_person", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            address=data.get("address", ""),
            notes=data.get("notes", ""),
            is_active=True,
            created_by=actor,
            updated_by=actor,
        )

        AuditService.log_event(
            action_code="stock.vendor.created",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(vendor.pk),
            actor_user=actor,
            company=company,
            before_snapshot=None,
            after_snapshot=snapshot(vendor),
        )

        return vendor

    @staticmethod
    def update_vendor(company, vendor_id, data: dict, actor):
        vendor = get_company_entity(
            Vendor, company, vendor_id,
            active_only=True, entity_name=ENTITY_TYPE,
        )
        before = snapshot(vendor)

        if "name" in data:
            new_name = data["name"].strip()
            new_normalized = normalize_name(data["name"])
            if new_normalized != vendor.normalized_name:
                if Vendor.objects.filter(
                    company=company, normalized_name=new_normalized,
                    is_active=True, is_deleted=False,
                ).exclude(pk=vendor.pk).exists():
                    raise StockConflictError(
                        f"Active vendor with name '{new_name}' already exists in this company"
                    )
                vendor.normalized_name = new_normalized
            vendor.name = new_name

        if "code" in data:
            new_code = data["code"]
            if new_code:
                new_code = normalize_code(new_code)
                if new_code != vendor.code:
                    if Vendor.objects.filter(
                        company=company, code=new_code,
                        is_active=True, is_deleted=False,
                    ).exclude(pk=vendor.pk).exists():
                        raise StockConflictError(
                            f"Active vendor with code '{new_code}' already exists in this company"
                        )
                vendor.code = new_code
            else:
                vendor.code = None

        for field in ("contact_person", "email", "phone", "address", "notes"):
            if field in data:
                setattr(vendor, field, data[field])

        vendor.updated_by = actor
        vendor.save()

        AuditService.log_event(
            action_code="stock.vendor.updated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(vendor.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(vendor),
        )

        return vendor

    @staticmethod
    def deactivate_vendor(company, vendor_id, actor):
        vendor = get_company_entity(
            Vendor, company, vendor_id,
            active_only=True, entity_name=ENTITY_TYPE,
        )

        model_count = ItemModel.objects.filter(
            company=company, vendor_reference=vendor,
            is_active=True, is_deleted=False,
        ).count()
        if model_count > 0:
            raise StockDeactivationBlockedError(
                entity_type=ENTITY_TYPE,
                reason=f"{model_count} active item models reference this vendor",
                blocking_count=model_count,
            )

        before = snapshot(vendor)
        vendor.is_active = False
        vendor.updated_by = actor
        vendor.save()

        AuditService.log_event(
            action_code="stock.vendor.deactivated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(vendor.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(vendor),
        )

        return vendor
