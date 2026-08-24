# Frontend

React and TypeScript application shell for CCDI.

## Run

```powershell
npm ci
npm run dev
```

Set `VITE_API_BASE_URL` in the repository `.env` when the API is not available at
`http://localhost:8000`.

## Organization

- `app`: process-wide providers and initialization
- `routes`, `pages`, `layouts`: navigation and page composition
- `features`: cohesive user-facing capabilities
- `components`: reusable, domain-neutral UI
- `api`, `hooks`, `stores`, `types`, `lib`: integration and shared foundations
- `graph`, `charts`, `gantt`, `ai`, `auth`, `i18n`: specialized platform boundaries

TanStack Query owns server state. Zustand is available only for complex client state that does not
belong in route state or local component state. Shared UI primitives should follow shadcn/ui
composition conventions and remain accessible and themeable.
# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the Oxlint configuration

If you are developing a production application, we recommend enabling type-aware lint rules by installing `oxlint-tsgolint` and editing `.oxlintrc.json`:

```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["react", "typescript", "oxc"],
  "options": {
    "typeAware": true
  },
  "rules": {
    "react/rules-of-hooks": "error",
    "react/only-export-components": ["warn", { "allowConstantExport": true }]
  }
}
```

See the [Oxlint rules documentation](https://oxc.rs/docs/guide/usage/linter/rules) for the full list of rules and categories.
