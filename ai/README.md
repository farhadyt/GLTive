<!-- Purpose: Documentation for the AI core infrastructure layer -->
# AI Core Infrastructure

The `ai/` package will house the AI core infrastructure for the GLTive platform.

## Future Scope (not implemented in this step)

- Local AI runtime
- Model hosting, registry, and versioning
- Inference orchestration and model routing
- Local/cloud fallback logic
- Prompt policy engine
- Context engine and memory isolation
- Tool calling fabric
- AI safety controls and approval policy
- AI logging and tenant AI governance

## AI Product Features (separate from AI Core)

- AI ticket triage
- AI summaries and incident explanations
- AI ops copilot / SOC copilot
- AI executive briefing
- AI recommendation engine

## Rules

- AI Core and AI Product Features are **separate** capabilities
- All AI actions must be audited and approval-aware
- Tenant memory isolation is mandatory
