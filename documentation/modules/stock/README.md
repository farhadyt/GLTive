# Stock & Inventory Foundation
Status: 🟡 IN PROGRESS
Last Updated: 2026-04-01

The Stock & Inventory Foundation is the foundational module capturing all raw assets, their lifecycle states, tracking configurations, and real-time physical locations for Phase 1.

## Scope
**In Scope:** Categories, brands, vendors, item models, warehouses, stock items, serial units, movements, adjustments, alerts, dashboard.
**Not in Scope for Phase 1:** Full asset lifecycle, comprehensive procurement tracking, HR linkage, complex QR/barcode generation.

## Entities
1. `stock_item_categories`
2. `brands`
3. `vendor_references`
4. `item_models`
5. `warehouses`
6. `stock_items`
7. `stock_serial_units`
8. `stock_movements`
9. `stock_adjustment_sessions`
10. `stock_adjustment_lines`
11. `stock_alert_rules`
12. `stock_alert_events`

## Services
1. Categories Service
2. Brands Service
3. Vendors Service
4. Item Models Service
5. Warehouses Service
6. Stock Items Service
7. Receive Quantity Service
8. Receive Serialized Service
9. Issue Quantity Service
10. Issue Serialized Service
11. Transfer Service
12. Adjustment Service
13. Alert Service

## API Endpoints
- Categories API
- Brands API
- Vendors API
- Item Models API
- Warehouses API
- Stock Items API
- Stock Receive API
- Stock Issue API
- Stock Transfer API
- Stock Adjustment API
- Stock Movement History API
- Stock Alerts API
- Stock Dashboard API
- Lookup/Reference API

## Permissions

| Permission Code | Description |
|-----------------|-------------|
| `stock.view` | View stock items and read-only data |
| `stock.manage` | Add or update stock items |
| `stock.master.manage` | Manage warehouses, vendors, and core dicts |
| `stock.receive` | Receive incoming stock items |
| `stock.issue` | Issue stock out to targets |
| `stock.transfer` | Move stock between internal warehouses |
| `stock.adjust` | Handle manual adjustment sessions |
| `stock.alert.manage` | Acknowledge/resolve threshold alerts |
| `stock.history.view` | View immutable movement history logs |

## Future Extension Hooks
- 🔵 **PLANNED:** Asset lifecycle mapping.
- 🔵 **PLANNED:** Procurement module integration.
- 🔵 **PLANNED:** Workforce assignment linkage.
- 🔵 **PLANNED:** QR/Barcoding logic.
- 🔵 **PLANNED:** AI Recommendation hooks.

> ℹ️ **NOTE:** Deep `data-model.md`, `api-contract.md`, and `service-rules.md` will be created when stock implementation begins.

## Related Documents
- [Platform Module Registry](../README.md)
