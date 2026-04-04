# Purpose: Critical service-layer tests for stock module business logic
"""
Stock Service Tests
Focused on the highest-risk business flows: transfer, receive, issue,
adjustment, and deactivation blocking.
"""
from decimal import Decimal

from django.test import TestCase

from modules.stock.models import StockItem, StockMovement, StockSerialUnit
from modules.stock.services import (
    CategoryService,
    StockAdjustmentService,
    StockIssueService,
    StockItemService,
    StockReceiveService,
    StockTransferService,
)
from modules.stock.services.exceptions import (
    StockConflictError,
    StockDeactivationBlockedError,
    StockNotFoundError,
    StockValidationError,
)
from modules.stock.tests.helpers import (
    create_brand,
    create_category,
    create_company,
    create_full_quantity_stock_item,
    create_item_model,
    create_stock_item,
    create_tenant,
    create_user,
    create_warehouse,
)


class ReceiveServiceTest(TestCase):
    def setUp(self):
        self.tenant = create_tenant()
        self.company = create_company(self.tenant)
        self.actor = create_user(self.company, is_company_admin=True)
        self.category = create_category(self.company, actor=self.actor)
        self.warehouse = create_warehouse(self.company, actor=self.actor)
        self.item_model = create_item_model(self.company, self.category, actor=self.actor)
        self.stock_item = create_stock_item(
            self.company, self.item_model, self.warehouse, actor=self.actor,
        )

    def test_quantity_receive_updates_quantities(self):
        result = StockReceiveService.receive_quantity_stock(
            company=self.company,
            data={"stock_item_id": self.stock_item.pk, "quantity": Decimal("50")},
            actor=self.actor,
        )
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity_on_hand, Decimal("50"))
        self.assertEqual(self.stock_item.quantity_available, Decimal("50"))
        self.assertIn("movement_id", result)

    def test_quantity_receive_creates_movement(self):
        StockReceiveService.receive_quantity_stock(
            company=self.company,
            data={"stock_item_id": self.stock_item.pk, "quantity": Decimal("10")},
            actor=self.actor,
        )
        self.assertEqual(
            StockMovement.objects.filter(
                company=self.company,
                stock_item=self.stock_item,
                movement_type=StockMovement.TYPE_STOCK_IN,
            ).count(),
            1,
        )

    def test_serialized_receive_creates_units(self):
        # Create serialized stock item
        serial_model = create_item_model(
            self.company, self.category, tracking_type="serialized",
            model_name="Serial Model", actor=self.actor,
        )
        serial_item = create_stock_item(
            self.company, serial_model, self.warehouse, actor=self.actor,
        )
        result = StockReceiveService.receive_serialized_stock(
            company=self.company,
            data={
                "stock_item_id": serial_item.pk,
                "units": [
                    {"serial_number": "SN-001"},
                    {"serial_number": "SN-002", "condition_status": "good"},
                ],
            },
            actor=self.actor,
        )
        self.assertEqual(len(result["serial_unit_ids"]), 2)
        serial_item.refresh_from_db()
        self.assertEqual(serial_item.quantity_on_hand, Decimal("2"))

    def test_receive_rejects_wrong_tracking_type(self):
        with self.assertRaises(StockValidationError):
            StockReceiveService.receive_serialized_stock(
                company=self.company,
                data={
                    "stock_item_id": self.stock_item.pk,
                    "units": [{"serial_number": "SN-X"}],
                },
                actor=self.actor,
            )


class IssueServiceTest(TestCase):
    def setUp(self):
        self.tenant = create_tenant()
        self.company = create_company(self.tenant)
        self.stock_item, self.warehouse, self.actor = create_full_quantity_stock_item(
            self.company, quantity=Decimal("100"),
        )

    def test_quantity_issue_reduces_correctly(self):
        StockIssueService.issue_quantity_stock(
            company=self.company,
            data={"stock_item_id": self.stock_item.pk, "quantity": Decimal("30")},
            actor=self.actor,
        )
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity_on_hand, Decimal("70"))
        self.assertEqual(self.stock_item.quantity_available, Decimal("70"))

    def test_issue_rejects_insufficient_stock(self):
        with self.assertRaises(StockValidationError):
            StockIssueService.issue_quantity_stock(
                company=self.company,
                data={"stock_item_id": self.stock_item.pk, "quantity": Decimal("999")},
                actor=self.actor,
            )

    def test_serialized_issue_rejects_foreign_serial_ids(self):
        """Serial unit IDs from another company must be rejected."""
        other_company = create_company(self.tenant, name="Company B", code="COMP-B")
        other_actor = create_user(other_company, username="other_actor", is_company_admin=True)
        other_cat = create_category(other_company, code="CAT-X", actor=other_actor)
        other_wh = create_warehouse(other_company, code="WH-X", actor=other_actor)
        other_model = create_item_model(
            other_company, other_cat, tracking_type="serialized",
            model_name="Other Serial", actor=other_actor,
        )
        other_item = create_stock_item(other_company, other_model, other_wh, actor=other_actor)
        result = StockReceiveService.receive_serialized_stock(
            company=other_company,
            data={
                "stock_item_id": other_item.pk,
                "units": [{"serial_number": "FOREIGN-SN-001"}],
            },
            actor=other_actor,
        )
        foreign_unit_id = result["serial_unit_ids"][0]

        # Create serialized item in our company
        serial_model = create_item_model(
            self.company, create_category(self.company, code="CAT-S", actor=self.actor),
            tracking_type="serialized", model_name="Our Serial", actor=self.actor,
        )
        our_item = create_stock_item(self.company, serial_model, self.warehouse, actor=self.actor)
        StockReceiveService.receive_serialized_stock(
            company=self.company,
            data={
                "stock_item_id": our_item.pk,
                "units": [{"serial_number": "OUR-SN-001"}],
            },
            actor=self.actor,
        )

        # Try to issue the foreign serial unit from our stock item
        with self.assertRaises(StockNotFoundError):
            StockIssueService.issue_serialized_stock(
                company=self.company,
                data={
                    "stock_item_id": our_item.pk,
                    "serial_unit_ids": [foreign_unit_id],
                },
                actor=self.actor,
            )


class TransferServiceTest(TestCase):
    def setUp(self):
        self.tenant = create_tenant()
        self.company = create_company(self.tenant)
        self.stock_item, self.warehouse, self.actor = create_full_quantity_stock_item(
            self.company, quantity=Decimal("100"),
        )
        self.target_warehouse = create_warehouse(
            self.company, code="WH-002", name="Target WH", actor=self.actor,
        )

    def test_successful_quantity_transfer(self):
        result = StockTransferService.transfer_quantity_stock(
            company=self.company,
            data={
                "source_stock_item_id": self.stock_item.pk,
                "target_warehouse_id": self.target_warehouse.pk,
                "quantity": Decimal("40"),
            },
            actor=self.actor,
        )
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity_on_hand, Decimal("60"))

        target = StockItem.objects.get(pk=result["target_stock_item_id"])
        self.assertEqual(target.quantity_on_hand, Decimal("40"))

    def test_transfer_cannot_create_negative_stock(self):
        with self.assertRaises(StockValidationError):
            StockTransferService.transfer_quantity_stock(
                company=self.company,
                data={
                    "source_stock_item_id": self.stock_item.pk,
                    "target_warehouse_id": self.target_warehouse.pk,
                    "quantity": Decimal("999"),
                },
                actor=self.actor,
            )

    def test_transfer_cannot_cross_company_boundaries(self):
        """Cannot transfer to a warehouse that belongs to another company."""
        other_company = create_company(self.tenant, name="Company B", code="COMP-B")
        other_actor = create_user(other_company, username="other_actor", is_company_admin=True)
        other_wh = create_warehouse(other_company, code="WH-OTHER", actor=other_actor)

        with self.assertRaises(StockNotFoundError):
            StockTransferService.transfer_quantity_stock(
                company=self.company,
                data={
                    "source_stock_item_id": self.stock_item.pk,
                    "target_warehouse_id": other_wh.pk,
                    "quantity": Decimal("10"),
                },
                actor=self.actor,
            )

    def test_transfer_reuses_existing_target_stock_item(self):
        # First transfer creates target
        result1 = StockTransferService.transfer_quantity_stock(
            company=self.company,
            data={
                "source_stock_item_id": self.stock_item.pk,
                "target_warehouse_id": self.target_warehouse.pk,
                "quantity": Decimal("20"),
            },
            actor=self.actor,
        )
        # Second transfer reuses target
        result2 = StockTransferService.transfer_quantity_stock(
            company=self.company,
            data={
                "source_stock_item_id": self.stock_item.pk,
                "target_warehouse_id": self.target_warehouse.pk,
                "quantity": Decimal("10"),
            },
            actor=self.actor,
        )
        self.assertEqual(result1["target_stock_item_id"], result2["target_stock_item_id"])
        target = StockItem.objects.get(pk=result2["target_stock_item_id"])
        self.assertEqual(target.quantity_on_hand, Decimal("30"))


class AdjustmentServiceTest(TestCase):
    def setUp(self):
        self.tenant = create_tenant()
        self.company = create_company(self.tenant)
        self.stock_item, self.warehouse, self.actor = create_full_quantity_stock_item(
            self.company, quantity=Decimal("50"),
        )

    def test_confirm_creates_correct_movements(self):
        session = StockAdjustmentService.create_adjustment_session(
            company=self.company,
            data={"warehouse_id": self.warehouse.pk},
            actor=self.actor,
        )
        StockAdjustmentService.upsert_adjustment_lines(
            company=self.company,
            session_id=session.pk,
            lines_data=[
                {"stock_item_id": self.stock_item.pk, "counted_quantity": Decimal("60")},
            ],
            actor=self.actor,
        )
        result = StockAdjustmentService.confirm_adjustment_session(
            company=self.company,
            session_id=session.pk,
            actor=self.actor,
        )
        self.assertEqual(result["status"], "confirmed")
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity_on_hand, Decimal("60"))

        # Check movement type
        adj_movements = StockMovement.objects.filter(
            company=self.company,
            stock_item=self.stock_item,
            movement_type=StockMovement.TYPE_ADJUSTMENT_PLUS,
        )
        self.assertEqual(adj_movements.count(), 1)
        self.assertEqual(adj_movements.first().quantity, Decimal("10"))

    def test_confirm_rejects_non_draft_session(self):
        session = StockAdjustmentService.create_adjustment_session(
            company=self.company,
            data={"warehouse_id": self.warehouse.pk},
            actor=self.actor,
        )
        StockAdjustmentService.upsert_adjustment_lines(
            company=self.company,
            session_id=session.pk,
            lines_data=[
                {"stock_item_id": self.stock_item.pk, "counted_quantity": Decimal("50")},
            ],
            actor=self.actor,
        )
        StockAdjustmentService.confirm_adjustment_session(
            company=self.company, session_id=session.pk, actor=self.actor,
        )
        # Trying to confirm again must fail
        with self.assertRaises(StockValidationError):
            StockAdjustmentService.confirm_adjustment_session(
                company=self.company, session_id=session.pk, actor=self.actor,
            )

    def test_adjustment_minus_updates_quantities(self):
        session = StockAdjustmentService.create_adjustment_session(
            company=self.company,
            data={"warehouse_id": self.warehouse.pk},
            actor=self.actor,
        )
        StockAdjustmentService.upsert_adjustment_lines(
            company=self.company,
            session_id=session.pk,
            lines_data=[
                {"stock_item_id": self.stock_item.pk, "counted_quantity": Decimal("30")},
            ],
            actor=self.actor,
        )
        StockAdjustmentService.confirm_adjustment_session(
            company=self.company, session_id=session.pk, actor=self.actor,
        )
        self.stock_item.refresh_from_db()
        self.assertEqual(self.stock_item.quantity_on_hand, Decimal("30"))
        self.assertEqual(self.stock_item.quantity_available, Decimal("30"))


class DeactivationBlockingTest(TestCase):
    def setUp(self):
        self.tenant = create_tenant()
        self.company = create_company(self.tenant)
        self.actor = create_user(self.company, is_company_admin=True)

    def test_category_deactivation_blocked_by_active_item_models(self):
        category = create_category(self.company, actor=self.actor)
        create_item_model(self.company, category, actor=self.actor)
        with self.assertRaises(StockDeactivationBlockedError):
            CategoryService.deactivate_category(
                company=self.company, category_id=category.pk, actor=self.actor,
            )

    def test_stock_item_deactivation_blocked_by_quantity(self):
        stock_item, _, actor = create_full_quantity_stock_item(
            self.company, quantity=Decimal("10"),
        )
        with self.assertRaises(StockDeactivationBlockedError):
            StockItemService.deactivate_stock_item(
                company=self.company, stock_item_id=stock_item.pk, actor=actor,
            )
