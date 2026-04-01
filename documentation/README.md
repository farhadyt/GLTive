# GLTive Platform Documentation
Status: 🟢 STABLE
Last Updated: 2026-04-01

GLTive is a vendor-controlled, modular, on-premise deployable, AI-driven enterprise IT operations platform combining asset, ticketing, monitoring, security, automation, and backup orchestration capabilities within a single multi-tenant skeleton.

## Documentation Map

| Section | Purpose | Status | Link |
|---------|---------|--------|------|
| [Architecture](architecture/README.md) | Core platform design, ADRs, tenant model | 🟢 STABLE | `./architecture` |
| [Modules](modules/README.md) | Business capability bounded contexts | 🟡 IN PROGRESS | `./modules` |
| [API](api/README.md) | API gateway contracts, response envelopes | 🟡 IN PROGRESS | `./api` |
| [Development](development/README.md) | Setup, conventions, code practices | 🟢 STABLE | `./development` |
| [Operations](operations/README.md) | Infrastructure, deployment, maintenance | 🟢 STABLE | `./operations` |
| [Changelog](changelog/CHANGELOG.md) | Release notes and platform history | 🟢 STABLE | `./changelog` |

## How to Navigate
These documents cover the technical foundation and operational instructions for the platform. Follow the links in the table above to dive into specific knowledge domains.

> ℹ️ **NOTE:** When any implementation step is completed, the corresponding documentation section must be updated in the same commit. A commit that adds or changes code without updating relevant documentation is considered incomplete.

## Status Legend
- 🟢 **STABLE**: Finalized, production-ready
- 🟡 **IN PROGRESS**: Actively being built
- 🔵 **PLANNED**: Not yet started
- 🔴 **DEPRECATED**: Superseded

## Related Documents
- [Platform Project Briefs](../about)
