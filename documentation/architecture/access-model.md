# Platform Access Model
> 🟢 **STABLE**

This document describes the minimal, DB-backed access mapping responsible for tenant isolation and permissions in the GLTive platform for Phase 1.

## Tenant Isolation Boundary

- **Vendor Level (`Tenant`):** The foundational global owner grouping. Vendor platforms manipulate groups of customer entities.
- **Customer Level (`Company`):** The operational isolation boundary. All business objects (orders, stock, staff) belong exclusively to a `Company`.
- **Identity Level (`User`):** Users must be bound to a `Company` (except explicit vendor/platform admins). 

Any request arriving at the backend goes through the `TenantMiddleware`, which explicitly populates `request.company` or sets it to `None`. 

## Permission Structure

To avoid heavy RBAC engineering prematurely, the platform uses a highly specific, minimal role implementation:

1. **Permissions:** Code-based literal records (e.g., `stock.view`, `order.manage`).
2. **Roles (`Role`):** Groupings of `Permissions`, strictly tied to a specific `Company`.
3. **Users (`User`):** Point to one `Role` containing explicit codes.

### Platform Flags
To facilitate fast operational boundaries, two explicitly structured flags exist on the `User` model:
- `is_platform_admin`: Super bypass. Users with this flag transcend company limits and manage platform-level configurations.
- `is_company_admin`: Admin bypass. Designates the owner or administrative actor for a specific `Company`, granting them functional bypass inside their tenant.

### The Guard Mechanism (API)
Most endpoints subclass `CompanyScopedViewSet` (from `core.api.base`), which natively overrides `get_queryset()` to enforce `filter(company=request.company)`. This acts as a robust firewall preventing data bleeding across companies, even if permissions are misconfigured.
