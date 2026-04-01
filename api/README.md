<!-- Purpose: Documentation for the API gateway layer -->
# API Gateway

The `api/` package manages versioned URL routing for all platform modules.

## URL Structure

```
/api/v1/stock/...     → Stock / Inventory module endpoints
/api/v1/...           → Future module endpoints
```

## Rules

- All endpoints are prefixed with `/api/v1/`
- Each module registers its own URL patterns
- URL configs are included here, not defined inline
- Authentication is enforced globally via DRF settings
