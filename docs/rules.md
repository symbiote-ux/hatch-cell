## Directory Layout (purpose)

```
src/
  app/            # Routes, layouts, global error boundaries, globals.css
  components/     # Reusable UI and feature components
    ui/           # shadcn-style primitives (button, card, input, dialog, ...)
    layouts/      # Layout components
  constants/      # Static content/config per domain
  contexts/       # React Context providers
  hooks/          # Custom hooks (auth session, responsive)
  lib/            # Cross-cutting libs (auth, security, prisma, email, utils)
    middleware/   # Modular middleware: security, rate limit, auth, CORS
  services/       # Domain services
  styles/         # Theme tokens (theme.ts) consumed by Tailwind config
prisma/           # Generated composed schema + migrations
``


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