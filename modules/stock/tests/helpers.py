# Purpose: Shared test fixtures and helpers for stock module tests
"""
Stock Test Helpers
Minimal factory functions for creating test entities with proper company isolation.
"""
from decimal import Decimal

from core.models import Company, Permission, Role, Tenant, User


def create_tenant(name="Test Tenant"):
    return Tenant.objects.create(name=name, slug=name.lower().replace(" ", "-"))


def create_company(tenant, name="Company A", code="COMP-A"):
    return Company.objects.create(tenant=tenant, name=name, code=code)


def create_user(company, username="testuser", password="testpass123!", **kwargs):
    user = User.objects.create_user(
        username=username,
        password=password,
        company=company,
        **kwargs,
    )
    return user


def create_user_with_permissions(company, username, perm_codes, password="testpass123!"):
    """Create a user with a role that has specific permission codes."""
    user = create_user(company, username=username, password=password)
    role = Role.objects.create(company=company, name=f"role_{username}")
    for code in perm_codes:
        perm, _ = Permission.objects.get_or_create(
            code=code, defaults={"name": code, "description": ""},
        )
        role.permissions.add(perm)
    user.role = role
    user.save()
    return user


def create_category(company, code="CAT-001", name="Test Category", actor=None):
    from modules.stock.services import CategoryService
    return CategoryService.create_category(
        company=company,
        data={"code": code, "name": name},
        actor=actor or _get_or_create_actor(company),
    )


def create_brand(company, name="Test Brand", actor=None):
    from modules.stock.services import BrandService
    return BrandService.create_brand(
        company=company,
        data={"name": name},
        actor=actor or _get_or_create_actor(company),
    )


def create_warehouse(company, code="WH-001", name="Main Warehouse", actor=None):
    from modules.stock.services import WarehouseService
    return WarehouseService.create_warehouse(
        company=company,
        data={"code": code, "name": name},
        actor=actor or _get_or_create_actor(company),
    )


def create_item_model(company, category, tracking_type="quantity_based",
                       model_name="Test Model", actor=None):
    from modules.stock.services import ItemModelService
    return ItemModelService.create_item_model(
        company=company,
        data={
            "category_id": category.pk,
            "model_name": model_name,
            "tracking_type": tracking_type,
        },
        actor=actor or _get_or_create_actor(company),
    )


def create_stock_item(company, item_model, warehouse, actor=None):
    from modules.stock.services import StockItemService
    return StockItemService.create_stock_item(
        company=company,
        data={
            "item_model_id": item_model.pk,
            "warehouse_id": warehouse.pk,
        },
        actor=actor or _get_or_create_actor(company),
    )


def create_full_quantity_stock_item(company, quantity=Decimal("100"), actor=None):
    """Create a fully set up quantity-based stock item with stock received."""
    from modules.stock.services import StockReceiveService
    actor = actor or _get_or_create_actor(company)
    category = create_category(company, actor=actor)
    warehouse = create_warehouse(company, actor=actor)
    item_model = create_item_model(company, category, actor=actor)
    stock_item = create_stock_item(company, item_model, warehouse, actor=actor)
    if quantity > 0:
        StockReceiveService.receive_quantity_stock(
            company=company,
            data={"stock_item_id": stock_item.pk, "quantity": quantity},
            actor=actor,
        )
        stock_item.refresh_from_db()
    return stock_item, warehouse, actor


def _get_or_create_actor(company):
    """Get or create a default actor user for a company."""
    user, _ = User.objects.get_or_create(
        username=f"actor_{company.code}",
        defaults={"company": company, "is_company_admin": True},
    )
    if not user.has_usable_password():
        user.set_password("testpass123!")
        user.save()
    return user


def get_jwt_token(user):
    """Obtain a JWT access token for the given user."""
    from rest_framework_simplejwt.tokens import AccessToken
    token = AccessToken.for_user(user)
    return str(token)


def authenticate_client(client, user):
    """Set JWT auth header on an APIClient for the given user."""
    token = get_jwt_token(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
