# Purpose: Critical API-layer tests for stock module endpoints
"""
Stock API Tests
Focused on auth/permission enforcement, tenant isolation, exception mapping,
and critical command/lookup endpoint behavior.

Uses JWT auth (not force_authenticate) so TenantMiddleware properly sets
request.company — this tests the real production auth path.
"""
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from core.models import Permission
from modules.stock.tests.helpers import (
    authenticate_client,
    create_company,
    create_full_quantity_stock_item,
    create_tenant,
    create_user,
    create_user_with_permissions,
    create_warehouse,
)


class AuthPermissionEnforcementTest(TestCase):
    """Verify that unauthenticated and unauthorized access is blocked."""

    def setUp(self):
        self.client = APIClient()
        self.tenant = create_tenant()
        self.company = create_company(self.tenant)

    def test_unauthenticated_access_rejected(self):
        response = self.client.get("/api/v1/stock/categories/")
        self.assertIn(response.status_code, [401, 403])

    def test_authenticated_without_permission_rejected(self):
        user = create_user(self.company, username="noperm")
        authenticate_client(self.client, user)
        response = self.client.get("/api/v1/stock/categories/")
        self.assertEqual(response.status_code, 403)

    def test_authenticated_with_permission_succeeds(self):
        user = create_user_with_permissions(
            self.company, "viewer", ["stock.view"],
        )
        authenticate_client(self.client, user)
        response = self.client.get("/api/v1/stock/categories/")
        self.assertEqual(response.status_code, 200)

    def test_company_admin_bypasses_permission(self):
        user = create_user(self.company, username="cadmin", is_company_admin=True)
        authenticate_client(self.client, user)
        response = self.client.get("/api/v1/stock/categories/")
        self.assertEqual(response.status_code, 200)


class TenantIsolationTest(TestCase):
    """Verify that company A cannot access company B data."""

    def setUp(self):
        self.client = APIClient()
        self.tenant = create_tenant()
        self.company_a = create_company(self.tenant, name="Company A", code="A")
        self.company_b = create_company(self.tenant, name="Company B", code="B")

    def test_list_only_shows_own_company_data(self):
        stock_a, _, _ = create_full_quantity_stock_item(self.company_a)
        stock_b, _, _ = create_full_quantity_stock_item(self.company_b)

        user_a = create_user_with_permissions(
            self.company_a, "viewer_a", ["stock.view"],
        )
        authenticate_client(self.client, user_a)
        response = self.client.get("/api/v1/stock/items/")
        self.assertEqual(response.status_code, 200)
        # StandardPagination wraps as: {"success": true, "data": {"items": [...]}}
        items = response.data.get("data", {}).get("items", [])
        item_ids = [item["id"] for item in items]
        self.assertIn(str(stock_a.pk), item_ids)
        self.assertNotIn(str(stock_b.pk), item_ids)

    def test_retrieve_foreign_item_returns_404(self):
        """Accessing a specific item from another company returns 404, not 403."""
        stock_b, _, _ = create_full_quantity_stock_item(self.company_b)
        user_a = create_user_with_permissions(
            self.company_a, "viewer_a2", ["stock.view"],
        )
        authenticate_client(self.client, user_a)
        response = self.client.get(f"/api/v1/stock/items/{stock_b.pk}/")
        self.assertEqual(response.status_code, 404)


class ExceptionMappingTest(TestCase):
    """Verify stock domain exceptions map to correct HTTP status codes."""

    def setUp(self):
        self.client = APIClient()
        self.tenant = create_tenant()
        self.company = create_company(self.tenant)
        self.user = create_user(self.company, username="admin", is_company_admin=True)
        authenticate_client(self.client, self.user)

    def test_validation_error_returns_400(self):
        response = self.client.post(
            "/api/v1/stock/categories/", data={}, format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_not_found_returns_404(self):
        import uuid
        fake_id = uuid.uuid4()
        response = self.client.get(f"/api/v1/stock/categories/{fake_id}/")
        self.assertEqual(response.status_code, 404)

    def test_conflict_returns_409(self):
        self.client.post(
            "/api/v1/stock/categories/",
            data={"code": "DUP-001", "name": "First"},
            format="json",
        )
        response = self.client.post(
            "/api/v1/stock/categories/",
            data={"code": "DUP-001", "name": "Second"},
            format="json",
        )
        self.assertEqual(response.status_code, 409)

    def test_error_envelope_structure(self):
        response = self.client.post(
            "/api/v1/stock/categories/", data={}, format="json",
        )
        self.assertEqual(response.status_code, 400)
        data = response.data
        self.assertFalse(data.get("success"))
        self.assertIn("error", data)
        error = data["error"]
        self.assertIn("code", error)
        self.assertIn("message", error)
        self.assertIn("field_errors", error)


class CommandEndpointTest(TestCase):
    """Verify critical command endpoints work with valid payloads."""

    def setUp(self):
        self.client = APIClient()
        self.tenant = create_tenant()
        self.company = create_company(self.tenant)
        self.user = create_user(self.company, username="admin", is_company_admin=True)
        authenticate_client(self.client, self.user)

    def test_receive_quantity_endpoint(self):
        stock_item, _, _ = create_full_quantity_stock_item(
            self.company, quantity=Decimal("0"),
        )
        response = self.client.post("/api/v1/stock/receive/quantity/", data={
            "stock_item_id": str(stock_item.pk),
            "quantity": "25.00",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data.get("success"))

    def test_transfer_quantity_endpoint(self):
        stock_item, wh, actor = create_full_quantity_stock_item(
            self.company, quantity=Decimal("50"),
        )
        target_wh = create_warehouse(
            self.company, code="WH-T", name="Target", actor=actor,
        )
        response = self.client.post("/api/v1/stock/transfer/quantity/", data={
            "source_stock_item_id": str(stock_item.pk),
            "target_warehouse_id": str(target_wh.pk),
            "quantity": "10.00",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get("success"))

    def test_adjustment_confirm_returns_success(self):
        stock_item, wh, _ = create_full_quantity_stock_item(
            self.company, quantity=Decimal("50"),
        )
        resp1 = self.client.post("/api/v1/stock/adjustments/", data={
            "warehouse_id": str(wh.pk),
        }, format="json")
        self.assertEqual(resp1.status_code, 201)
        session_id = resp1.data["data"]["id"]

        resp2 = self.client.put(
            f"/api/v1/stock/adjustments/{session_id}/lines/",
            data={
                "lines_data": [
                    {"stock_item_id": str(stock_item.pk), "counted_quantity": "55.00"},
                ],
            },
            format="json",
        )
        self.assertEqual(resp2.status_code, 200)

        resp3 = self.client.post(f"/api/v1/stock/adjustments/{session_id}/confirm/")
        self.assertEqual(resp3.status_code, 200)
        self.assertTrue(resp3.data.get("success"))


class LookupEndpointTest(TestCase):
    """Verify lookup endpoints require auth and are company-scoped."""

    def setUp(self):
        self.client = APIClient()
        self.tenant = create_tenant()
        self.company = create_company(self.tenant)

    def test_lookup_requires_auth(self):
        response = self.client.get("/api/v1/stock/lookups/categories/")
        self.assertIn(response.status_code, [401, 403])

    def test_lookup_returns_own_company_data(self):
        from modules.stock.tests.helpers import create_category
        user = create_user_with_permissions(
            self.company, "viewer_lk", ["stock.view"],
        )
        create_category(self.company, code="LK-CAT", actor=user)

        other_company = create_company(self.tenant, name="Other", code="OTH")
        other_user = create_user(other_company, username="other_lk", is_company_admin=True)
        create_category(other_company, code="OTHER-CAT", actor=other_user)

        authenticate_client(self.client, user)
        response = self.client.get("/api/v1/stock/lookups/categories/")
        self.assertEqual(response.status_code, 200)
        # Lookup viewsets have pagination_class=None — DRF returns raw list
        data = response.data
        if isinstance(data, dict):
            data = data.get("data", data)
        codes = [c["code"] for c in data]
        self.assertIn("LK-CAT", codes)
        self.assertNotIn("OTHER-CAT", codes)


class PermissionBootstrapTest(TestCase):
    """Verify the stock permission bootstrap command works."""

    def test_bootstrap_creates_all_permissions(self):
        from django.core.management import call_command
        from io import StringIO

        out = StringIO()
        call_command("bootstrap_stock_permissions", stdout=out)
        output = out.getvalue()
        self.assertIn("bootstrap complete", output)

        expected_codes = [
            "stock.view", "stock.manage", "stock.master.manage",
            "stock.receive", "stock.issue", "stock.transfer",
            "stock.adjust", "stock.alert.manage", "stock.history.view",
        ]
        for code in expected_codes:
            self.assertTrue(
                Permission.objects.filter(code=code).exists(),
                f"Permission '{code}' should exist after bootstrap",
            )

    def test_bootstrap_is_idempotent(self):
        from django.core.management import call_command
        from io import StringIO

        call_command("bootstrap_stock_permissions", stdout=StringIO())
        call_command("bootstrap_stock_permissions", stdout=StringIO())

        stock_perms = Permission.objects.filter(code__startswith="stock.").count()
        self.assertEqual(stock_perms, 9)
