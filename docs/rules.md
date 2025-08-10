

### Tech Stack

- Next.js 15 (App Router), React 18, TypeScript (strict)
- Tailwind CSS + shadcn/ui primitives
- Prisma ORM (PostgreSQL)
- Testing: Vitest + React Testing Library
- Infra: Vercel/AWS-ready; S3 for images

---

## Directory Layout (purpose)

```
src/
  app/            # Routes, layouts, global error boundaries, globals.css
  components/     # Reusable UI and feature components
    ui/           # shadcn-style primitives (button, card, input, dialog, ...)
    layouts/      # Layout components
  constants/      # Static content/config per domain (home, school, etc.)
  contexts/       # React Context providers
  hooks/          # Custom hooks (auth session, performance, responsive)
  lib/            # Cross-cutting libs (auth, security, prisma, email, utils)
    middleware/   # Modular middleware: security, rate limit, auth, CORS
    utils/        # cn(), icons, image-resize, map, filter utils (re-exports)
  services/       # Domain services (school, seo, student, teacher)
  styles/         # Theme tokens (theme.ts) consumed by Tailwind config
  types/          # Shared TypeScript types

prisma/           # Generated composed schema + migrations
prisma-config/    # Modular prisma models + `merge-prisma-schema.ts`
scripts/          # Security, seeding, analysis scripts
docs/             # SPEC, AUTHENTICATION, SECURITY_SETUP, TESTING, etc.
```

---

## Coding Rules & Conventions

- TypeScript
  - `strict: true`; path alias `@/*` → `src/*`
  - Prefer interfaces for objects; explicit return types for exported APIs
  - Disallow `any`; unused variables must be prefixed with `_`
- ESLint/Prettier
  - Extends `next/core-web-vitals` and `@typescript-eslint/recommended`
  - Prettier: `printWidth: 120`, `singleQuote: true`
- Naming
  - Components (feature): PascalCase files; UI primitives: lower-case file names (e.g., `button.tsx`)
  - Variables/functions: camelCase; constants: UPPER_CASE
- React
  - Functional components; typed props; use `forwardRef` for primitives
  - Keep files under 500 LOC; extract hooks/utils when growing
- Imports
  - Relative within feature; use `@/` for cross-feature/shared
- Comments
  - Explain “why” for non-obvious logic; avoid trivial commentary

---

## Styling Rules

- Tailwind
  - Dark mode via `class`
  - Tokens defined in `src/styles/theme.ts` and exposed in Tailwind via `tailwind.config.ts`
  - Breakpoints: `sm 640`, `md 768`, `lg 1024`, `xl 1280`, `2xl 1536`
  - Colors via CSS variables (`:root` / `.dark`): `--background`, `--primary`, etc. consumed as `hsl(var(--token))`
  - Custom utilities in `globals.css`: `.scrollbar-hide`, `.line-clamp-3`, `.line-clamp-4`
  - Focus patterns: `focus-visible:ring-*` consistent across inputs/buttons
- shadcn/ui primitives
  - Live in `src/components/ui/*`; built with `cva` and `cn()`
  - Standard variant/size APIs with typed `VariantProps`
  - Example: button variants (`variant: default|destructive|outline|secondary|ghost|link`; `size: sm|default|lg|icon`)
- Spacing & layout
  - Section wrapper (`ui/section.tsx`) standardizes vertical rhythm:
    - `sm: py-8`, `md: py-12`, `lg: py-16`, `xl: py-20`; centers with `mx-auto` + `max-w-*`
- Animation
  - `tailwindcss-animate` + small custom keyframes (e.g., accordion)

---

## Component, Hooks, and Utility Patterns

- Class composition
  - `cn(...classes)` using `clsx` + `tailwind-merge` to dedupe
  - `cva` for typed variants; expose `VariantProps<typeof variants>`
- UI primitives
  - Forward refs; accessible focus states; disabled states unified
  - Compound components: `Card`, `CardHeader`, `CardContent`, `CardFooter`, etc.
- Hooks
  - `useIsMobile(breakpoint=768)` resize breakpoint detection
  - `usePerformance`: `useDebounce`, `useIntersectionObserver`, timers, and insights
- Utils
  - Re-export URL filter helpers from services; image resize, map/location utilities

---

## Data, Security, and Middleware

- Prisma workflow
  - Maintain models in `prisma-config/models/*.prisma`
  - Compose schema: `npm run prisma:build` (runs `merge-prisma-schema.ts`)
  - Generate/migrate: `npm run prisma:migrate` (build + `prisma migrate dev`)
- Security
  - Middleware layers: security headers, attack/bot detection, auth protection (route/role map), rate limiting, CORS on `/api/*`
  - Next config: strict security headers; remove source maps in prod; optional bundle analyzer via `ANALYZE=true`
- Images
  - Whitelisted remote hosts (Unsplash, placeholders, S3 buckets); formats: `webp`, `avif`

---

## Testing & Tooling

- Vitest + React Testing Library; `jsdom` environment; setup mocks in `test/setup.ts`
- Core commands
  - `npm test` | watch `npm run test:watch` | coverage `npm run test:coverage`
  - Security: `npm run test:security`, `npm run security:audit`
  - Lint/format/type: `npm run lint`, `npm run lint:fix`, `npm run format`, `npm run type-check`

---

## Build & Run

- Dev: `npm run dev` (Turbopack)
- Build: `npm run build` (runs `prisma generate` + Next build)
- Start: `npm start`
- Analyze: `npm run analyze` (sets `ANALYZE=true`)

---

## Environment (examples)

```
DATABASE_URL=postgresql://username:password@localhost:5432/schoolo
NEXTAUTH_SECRET=your-secret
NEXTAUTH_URL=http://localhost:3000
NEXT_PUBLIC_SITE_URL=http://localhost:3000

# AWS (if using Dynamo or S3 services)
AWS_REGION=ap-south-1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...

# Optional SMTP (prod)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=...
SMTP_PASS=...
SMTP_FROM=noreply@schoolo.com
```

---

## Project Memory Prompt 

```
Architecture & Structure
- Next.js App Router with TypeScript (strict). Alias @/ → src/. Files < 500 LOC.
- Layout: src/app, src/components (ui primitives in src/components/ui), src/constants, src/contexts, src/hooks, src/lib (auth/security/prisma/utils), src/services, src/styles/theme.ts, src/types.
- Relative imports within feature; use @/ for cross-feature.

TypeScript & Linting
- Disallow any; explicit return types for exported functions; unused vars prefixed _ are ignored.
- ESLint extends next/core-web-vitals + @typescript-eslint; Prettier printWidth 120, singleQuote true.

React & Components
- Functional components; forwardRef for primitives; typed props.
- UI primitives use cva variants and cn() class merge; accessible focus states.
- Section wrapper provides variant/size/maxWidth/centered and sets vertical rhythm.

Styling (Tailwind + Theme)
- Dark mode via class. Theme tokens live in src/styles/theme.ts (breakpoints, colors, spacing, typography, shadows, zIndex, radii).
- Colors via CSS variables in globals.css and mapped with hsl(var(--token)).
- Utilities: .scrollbar-hide and .line-clamp-(3|4|none). Focus rings standardized.

Data & Services
- Prisma schema modularized in prisma-config/models; compose via merge-prisma-schema.ts.
- Domain services in src/services/<domain>; cross-cutting in src/lib.

Security & Middleware
- Modular middleware: security headers, attack/bot detection, role-based auth, rate limiting, CORS on /api/*.
- next.config: remove prod source maps, image host whitelist, standalone output, optional analyzer.

Testing
- Vitest + RTL, jsdom; setup mocks for Next router/Image/Link, observers. Alias @ → src in vitest and vite configs.

Build & Tooling
- Dev: next dev --turbopack; Build: prisma generate + next build.
- Lint-staged runs eslint --fix and prettier on staged TS/TSX. Type-check in CI.

Conventions
- Naming: PascalCase components (feature), lower-case file names for ui primitives. camelCase vars/functions, UPPER_CASE constants.
- No magic numbers—use constants or theme tokens. Extract hooks/utils to keep components focused.
```

---