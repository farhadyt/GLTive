# Purpose: Business service for StockCategory master data
"""
Category Service
Company-scoped CRUD and deactivation logic for stock categories.
"""
from django.db import transaction

from audit.services.logger import AuditService
from modules.stock.models.category import StockCategory
from modules.stock.models.item_model import ItemModel
from modules.stock.services.exceptions import (
    StockConflictError,
    StockDeactivationBlockedError,
    StockValidationError,
)
from modules.stock.services.utils import (
    get_company_entity,
    normalize_code,
    snapshot,
)

ENTITY_TYPE = "stock_category"


class CategoryService:
    """Business logic for stock category management."""

    @staticmethod
    def create_category(company, data: dict, actor):
        code = data.get("code")
        name = data.get("name")

        if not code:
            raise StockValidationError("code is required", field="code")
        if not name:
            raise StockValidationError("name is required", field="name")

        code = normalize_code(code)

        # Duplicate check
        if StockCategory.objects.filter(
            company=company, code=code, is_deleted=False
        ).exists():
            raise StockConflictError(
                f"Active category with code '{code}' already exists in this company"
            )

        # Parent validation
        parent_category = None
        parent_id = data.get("parent_category_id")
        if parent_id:
            parent_category = get_company_entity(
                StockCategory, company, parent_id,
                active_only=True, entity_name=ENTITY_TYPE,
            )

        category = StockCategory.objects.create(
            company=company,
            code=code,
            name=name.strip(),
            description=data.get("description", ""),
            parent_category=parent_category,
            sort_order=data.get("sort_order", 0),
            is_active=True,
            created_by=actor,
            updated_by=actor,
        )

        AuditService.log_event(
            action_code="stock.category.created",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(category.pk),
            actor_user=actor,
            company=company,
            before_snapshot=None,
            after_snapshot=snapshot(category),
        )

        return category

    @staticmethod
    def update_category(company, category_id, data: dict, actor):
        category = get_company_entity(
            StockCategory, company, category_id,
            active_only=True, entity_name=ENTITY_TYPE,
        )
        before = snapshot(category)

        # Code change
        if "code" in data:
            new_code = normalize_code(data["code"])
            if new_code != category.code:
                if StockCategory.objects.filter(
                    company=company, code=new_code, is_deleted=False,
                ).exclude(pk=category.pk).exists():
                    raise StockConflictError(
                        f"Active category with code '{new_code}' already exists in this company"
                    )
                category.code = new_code

        if "name" in data:
            category.name = data["name"].strip()

        if "description" in data:
            category.description = data["description"]

        if "sort_order" in data:
            category.sort_order = data["sort_order"]

        # Parent change
        if "parent_category_id" in data:
            parent_id = data["parent_category_id"]
            if parent_id is None:
                category.parent_category = None
            else:
                if str(parent_id) == str(category.pk):
                    raise StockValidationError(
                        "A category cannot be its own parent",
                        field="parent_category_id",
                    )
                parent = get_company_entity(
                    StockCategory, company, parent_id,
                    active_only=True, entity_name=ENTITY_TYPE,
                )
                # Cyclic hierarchy detection
                ancestor = parent
                depth = 0
                while ancestor.parent_category_id is not None:
                    depth += 1
                    if depth > 50:
                        raise StockValidationError("Category hierarchy too deep")
                    if str(ancestor.parent_category_id) == str(category.pk):
                        raise StockValidationError(
                            "Cyclic category hierarchy detected",
                            field="parent_category_id",
                        )
                    ancestor = get_company_entity(
                        StockCategory, company, ancestor.parent_category_id,
                        entity_name=ENTITY_TYPE,
                    )
                category.parent_category = parent

        category.updated_by = actor
        category.save()

        AuditService.log_event(
            action_code="stock.category.updated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(category.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(category),
        )

        return category

    @staticmethod
    def deactivate_category(company, category_id, actor):
        category = get_company_entity(
            StockCategory, company, category_id,
            active_only=True, entity_name=ENTITY_TYPE,
        )

        # Blocker 1: active child categories
        child_count = StockCategory.objects.filter(
            company=company, parent_category=category,
            is_active=True, is_deleted=False,
        ).count()
        if child_count > 0:
            raise StockDeactivationBlockedError(
                entity_type=ENTITY_TYPE,
                reason=f"{child_count} active child categories exist",
                blocking_count=child_count,
            )

        # Blocker 2: active item models
        model_count = ItemModel.objects.filter(
            company=company, category=category,
            is_active=True, is_deleted=False,
        ).count()
        if model_count > 0:
            raise StockDeactivationBlockedError(
                entity_type=ENTITY_TYPE,
                reason=f"{model_count} active item models reference this category",
                blocking_count=model_count,
            )

        before = snapshot(category)
        category.is_active = False
        category.updated_by = actor
        category.save()

        AuditService.log_event(
            action_code="stock.category.deactivated",
            target_entity_type=ENTITY_TYPE,
            target_entity_id=str(category.pk),
            actor_user=actor,
            company=company,
            before_snapshot=before,
            after_snapshot=snapshot(category),
        )

        return category
