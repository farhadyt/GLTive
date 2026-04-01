<!-- Purpose: Documentation for the localization and i18n infrastructure -->
# Localization

The `localization/` package manages multi-language support for the GLTive platform.

## Supported Languages

| Code | Language    | Direction |
|------|-------------|-----------|
| `az` | Azerbaijani | LTR       |
| `ru` | Russian     | LTR       |
| `en` | English     | LTR       |
| `tr` | Turkish     | LTR       |
| `ar` | Arabic      | RTL       |

## Structure

```
localization/
└── locale/
    ├── az/LC_MESSAGES/    → Azerbaijani translations
    ├── ru/LC_MESSAGES/    → Russian translations
    ├── en/LC_MESSAGES/    → English translations
    ├── tr/LC_MESSAGES/    → Turkish translations
    └── ar/LC_MESSAGES/    → Arabic translations
```

## Rules

- **No hardcoded strings** — all user-facing text uses Django's `gettext` / `gettext_lazy`
- Notification templates are also localization-ready
- Date, time, and number formats are locale-aware
- Arabic requires RTL-readiness in the future frontend
- Translation governance process to be defined

## Commands

```bash
# Extract translation strings
python manage.py makemessages -l az -l ru -l en -l tr -l ar

# Compile translations
python manage.py compilemessages
```
