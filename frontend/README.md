# GLTive Web Frontend

Web management interface for the GLTive enterprise IT operations platform.

## Stack

- **Build:** Vite
- **Framework:** React 18 + TypeScript (strict)
- **Styling:** TailwindCSS v4
- **Routing:** React Router v7
- **Server State:** TanStack Query v5
- **Forms:** React Hook Form + Zod
- **i18n:** react-i18next (5 languages: EN, AZ, RU, TR, AR with RTL)
- **HTTP:** Axios
- **Icons:** Lucide React

## Architecture

The frontend is a standalone SPA, separate from the Django backend.
In development, Vite proxies `/api` requests to the Django server at `localhost:8000`.

```
src/
  app/          — App entry, router, guards, login page
  modules/      — Feature modules (mirrors backend bounded contexts)
    stock/      — Stock module pages and components
  shared/
    ui/         — Design system components (Button, Input, Modal, DataTable, etc.)
    layouts/    — Shell components (Sidebar, TopBar, AppShell)
    lib/        — Auth, API client, permissions, JWT decode
    hooks/      — Shared hooks (useTheme)
    config/     — Navigation, permission constants
    types/      — TypeScript type definitions
  i18n/         — Translation files and i18n config
  styles/       — Global CSS, design tokens
```

## Development

```bash
cd frontend
npm install
npm run dev    # starts at http://localhost:3000
```

Backend must be running at `localhost:8000` for API proxy to work.

## Auth Model (current stage)

- JWT tokens stored **in-memory only** (not localStorage).
- Hard browser reload clears session — user must re-login.
- 401 responses trigger a silent refresh attempt; if refresh fails, user is redirected to login.
- Backend JWT claims include: `company_id`, `is_platform_admin`, `is_company_admin`.
- **Fine-grained role permissions are NOT yet in JWT.** Only admin users (platform_admin / company_admin) currently pass permission checks. Non-admin permission enforcement will activate when backend provides a permission source (JWT extension or /me endpoint).

## What This Foundation Includes

- App shell with collapsible sidebar, topbar, dark/light theme
- Auth flow: login, logout, 401 recovery, token refresh
- Permission-aware routing and rendering (admin-only active currently)
- API client with auth injection and error normalization
- TanStack Query provider
- i18n with 5 languages and Arabic RTL switching
- 14 shared UI components
- Stock module placeholder pages

## What This Foundation Does NOT Include

- Real stock business screens (tables, forms, workflows)
- Visual design polish (will be guided by Google Stitch design direction)
- Non-admin fine-grained permission enforcement
- Persistent session across browser reload
- Backend /me endpoint integration
