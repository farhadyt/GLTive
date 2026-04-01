# API Documentation
Status: 🟡 IN PROGRESS
Last Updated: 2026-04-01

GLTive relies on a strict, namespaced RESTful API using JSON envelopes. By adhering to uniform request and response contracts, frontend logic and subsequent module integrations remain highly predictable.

## API Design Principles
- **Company-scoped**: All applicable endpoints authenticate and implicitly filter on the user's active company context.
- **Command-style endpoints**: Operations aren't strictly CRUD-only; explicit commands are used for complex state shifts.
- **Immutable history**: Endpoints prefer issuing discrete transactional events rather than updating records silently in place.
- **Backend enforcement**: All validations happen server-side; UI only reflects engine capabilities.
- **Audit by default**: Every mutation leaves a trace.

**Base URL**: `/api/v1/`

## Response Envelopes

**Success Format**
```json
{
    "success": true,
    "message": "item_created_successfully",
    "data": {
        "id": "uuid"
    },
    "meta": {}
}
```

**Error Format**
```json
{
    "success": false,
    "error": {
        "code": "validation_error",
        "message": "invalid_payload",
        "details": {},
        "field_errors": {
            "name": ["This field is required."]
        }
    }
}
```

**Pagination Format**
```json
{
    "success": true,
    "data": {
        "items": [],
        "pagination": {
            "page": 1,
            "page_size": 20,
            "total_items": 140,
            "total_pages": 7
        }
    }
}
```

## HTTP Status Codes

| Status | When Used |
|--------|-----------|
| `200` | Successful read, update, or command |
| `201` | Successful entity creation |
| `400` | Validation failures, malformed syntax |
| `403` | Authentication valid, but user lacks permissions |
| `404` | Requested object/route does not exist |
| `409` | Conflict (e.g. duplicate unique entries) |

## Authentication
GLTive uses JWT for stateless token evaluation. Tokens must be passed in the `Authorization` header.

```http
Authorization: Bearer <token>
```

> ℹ️ **NOTE:** Detailed endpoint docs live in each module's `api-contract.md`.

## Related Documents
- [Development Workflow](../development/README.md)
