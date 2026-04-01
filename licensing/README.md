<!-- Purpose: Documentation for the licensing and entitlement engine -->
# Licensing & Entitlement Engine

The `licensing/` package will manage module activation, entitlements,
and commercial control for the GLTive platform.

## Future Scope (not implemented in this step)

- Vendor License & Entitlement Server integration
- Local License Agent
- Signed entitlement packages
- Online sync activation
- Offline package activation
- Runtime enforcement
- Hybrid packaging (built-in locked + separately signed)
- Installation identity (environment-bound)

## Pricing Model Foundation

```
Price = Base Platform Fee
      + Activated Module Fee
      + Managed Resource Units
      + Site/Instance Factor
      + Optional Premium AI/SOC/Advanced Modules
```

## Rules

- Module activation is via signed entitlements, **not** source code flags
- Licensing is enforced at runtime, not just at deployment
- Connected and air-gapped activation modes must both be supported
