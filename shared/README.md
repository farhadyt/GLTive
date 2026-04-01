<!-- Purpose: Documentation for the shared utilities package -->
# Shared

Cross-cutting utilities, mixins, base serializers, and helpers used across
all modules of the GLTive platform.

## Contents

| Sub-package      | Purpose                                         |
|------------------|-------------------------------------------------|
| `serializers/`   | Base serializer classes with standard patterns   |
| `pagination/`    | Standard pagination configuration                |
| `exceptions/`    | Custom exception handler for consistent API errors |
| `responses/`     | Standard API response wrapper                    |
| `utils/`         | General utility functions                        |

## Rules

- This package **must not** contain business logic
- This package **must not** import from any module under `modules/`
- Only `core` and third-party imports are allowed
