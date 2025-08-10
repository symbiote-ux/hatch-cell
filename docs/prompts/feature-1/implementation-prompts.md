# Implementation Prompts (Step-by-Step)

These prompts drive a code-generation LLM to implement HatchCell in safe, incremental slices. Each prompt ends with wiring so there are no orphaned changes.

---

## Prompt 0.1 — Foundations: Routing, Tailwind, Base Pages

```text
Goal: Initialize routing skeleton and Tailwind. Create pages `/`, `/briefs`, `/briefs/[slugId]`, `/auth/signin`.

Requirements:
- Configure Tailwind and shadcn/ui (scaffold only; minimal components).
- Add a basic `layout.tsx` with metadata and top nav linking to Home and Briefs.
- Implement server components for the pages with placeholder content and TODO markers.
- Ensure ESLint and TypeScript checks pass.

Wiring:
- Add links between pages; confirm navigation works in dev.
- Add `npm` scripts: dev, build, lint, typecheck.
```

---

## Prompt 1.1 — Auth.js with Google + Email (JWT)

```text
Goal: Add Auth.js with Google and Email providers; stateless JWT sessions.

Requirements:
- Create `app/api/auth/[...nextauth]/route.ts` with providers and JWT callbacks.
- Add session retrieval helpers for server components and API routes.
- Add `/auth/signin` page with provider buttons.
- Add `NEXTAUTH_SECRET`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `EMAIL_FROM`, `EMAIL_SERVER` to env reading.

Wiring:
- Show user name/avatar in nav when signed in; sign in/out actions.
- Protect `/briefs/new` with auth; redirect to `/auth/signin` if not signed in.
```

---

## Prompt 1.2 — Minimal Profiles

```text
Goal: Implement minimal founder/student profiles with guardrails.

Requirements:
- Add Prisma models: `User`, `ProfileFounder`, `ProfileStudent` (1-1).
- Create `/profile` page to capture minimal fields per spec.
- Implement server actions to create/update profiles tied to current user.
- Add middleware/guards so post/apply flows require completed minimal profile.

Wiring:
- Add callouts on `/` and `/briefs` prompting profile completion if missing.
```

---

## Prompt 2.1 — Briefs Schema and Seeding

```text
Goal: Add Prisma models for Brief and Skill; migration and seed.

Requirements:
- Implement `Brief`, `Skill` per spec (trim non-critical fields if needed initially).
- Add slug + shortId generation utilities with validation rules.
- Create migration and seed with sample skills and 3 sample published briefs.

Wiring:
- Add a basic repository/service layer to create/list briefs.
```

---

## Prompt 2.2 — Brief Creation Wizard (Draft)

```text
Goal: Implement Draft creation at `/briefs/new` with validation.

Requirements:
- Multi-step form (can be single page initially) capturing required fields.
- Server actions or API to persist Drafts; owner-only access.
- Client-side validation reflecting limits in spec.

Wiring:
- On save, navigate to `/briefs/{slug}-{shortId}` (shows Draft badge to owner only).
```

---

## Prompt 2.3 — Publish/Unlist Lifecycle (no OTP yet)

```text
Goal: Implement status transitions and public visibility.

Requirements:
- API endpoints per spec for publish/unlist/republish.
- Listing respects status; detail page visible only when Published (unless owner).
- Applications toggle default Open on publish.

Wiring:
- Add controls on owner view to publish/unlist.
- Update `/briefs` list to show published items.
```

---

## Prompt 3.1 — Briefs Listing and Pagination

```text
Goal: Public `/briefs` list with pagination (page/limit; cursor later).

Requirements:
- Server-rendered list reading from DB with filters stubbed.
- Add page param; show total count; simple pagination controls.

Wiring:
- Cards link to detail; homepage grid shows latest 6.
```

---

## Prompt 3.2 — Filters and Keyword Search

```text
Goal: Add filters and keyword search across fields.

Requirements:
- Filter by required skills, experience, compensation, duration, availability, timezone.
- Keyword search across Title, Problem, Key features, Required skills, Deliverables, Target users.
- For SQLite, use `LIKE`; move to Postgres ILIKE later.

Wiring:
- Preserve query state in URL; reset controls.
```

---

## Prompt 3.3 — Most Active Sort

```text
Goal: Add computed sort using Applications and Messages counts in last 7 days.

Requirements:
- Add lightweight counters via queries; no stored score.
- Toggle sort control between Latest and Most active.

Wiring:
- Ensure tie-break by publish date desc.
```

---

## Prompt 4.1 — Applications (MVP)

```text
Goal: Implement application submit/update/withdraw.

Requirements:
- Prisma `Application` model; server actions/APIs to create/update/withdraw.
- Enforce one active application per user per brief.
- Applicant must have profile complete; auth required.

Wiring:
- Founder sees applications list on brief owner view.
- Applicant sees their submitted application on detail.
```

---

## Prompt 4.2 — Messaging (Application Thread)

```text
Goal: Text-only messaging thread tied to application; polling every 10s.

Requirements:
- Models: `MessageThread`, `Message` with type=Application.
- Create thread on first application; enforce participants.
- Add API to list/send messages; client polls every 10s.

Wiring:
- Thread UI under application detail for both parties.
```

---

## Prompt 5.1 — Projects on Accept

```text
Goal: Accepting an application creates a project and a project-level thread.

Requirements:
- Status transitions: Pending -> Accepted/Rejected; Undo within 24h.
- On Accept, create `Project` with participants and initialize messages thread.
- Route `/projects/{id}` renders Overview tab with summary fields.

Wiring:
- Notifications stubbed (console/log) for now.
```

---

## Prompt 5.2 — Milestones CRUD

```text
Goal: Milestones with statuses and optional fields.

Requirements:
- Models: `Milestone`, `MilestoneChecklistItem`.
- CRUD APIs; permissions for Founder/Co-builder; mentors read/comment.
- UI: List, create, edit status, reorder checklist items.

Wiring:
- Link from project Overview to Milestones tab.
```

---

## Prompt 6.1 — File Uploads (Local Stub)

```text
Goal: Enable PDF resume upload and brief asset uploads locally.

Requirements:
- Validate MIME and size (PDF <= 10MB; assets up to 10 files, 50MB total).
- Implement local adapter (temp dir) and presign-like interface.

Wiring:
- Attach resume to application; preview link.
```

---

## Prompt 6.2 — S3 Presigned Uploads + CloudFront

```text
Goal: Swap to S3 adapter with presigned PUT and CloudFront public reads.

Requirements:
- Env: `AWS_REGION`, `AWS_S3_BUCKET`, `CLOUDFRONT_URL`.
- Secure presign endpoints; store keys/URLs; enforce limits.

Wiring:
- Replace local adapter behind interface; zero UI changes.
```

---

## Prompt 7.1 — OTP (Stub)

```text
Goal: Add phone OTP request/verify flow without SMS provider.

Requirements:
- Endpoints: `/api/otp/request`, `/api/otp/verify` with in-memory or DB codes.
- Associate verified phone with user.
- Block publish/apply until verified per role.

Wiring:
- Add phone capture UI; show verification state in profile.
```

---

## Prompt 7.2 — OTP via SNS + Limits

```text
Goal: Integrate AWS SNS for SMS and enforce rate limits.

Requirements:
- Env: `SNS_SENDER_ID`, `OTP_*` knobs from spec; India-only check.
- Persist attempts and lockouts; audit via `RateLimitEvent`.

Wiring:
- Replace stub sender with SNS client; add server-side validation messages.
```

---

## Prompt 7.3 — Rate Limits for Apply/Messaging

```text
Goal: Enforce per-thread and per-day caps for applications and messages.

Requirements:
- Implement windowed counters and 429 responses; expose remaining quota in headers.

Wiring:
- Show UI toasts when limits are hit; disable send/apply temporarily.
```

---

## Prompt 8.1 — Admin & Moderation

```text
Goal: Admin dashboard for review and moderation.

Requirements:
- Routes `/admin`, `/admin/review` gated by email whitelist.
- Actions: takedown/restore, feature/unfeature, suspend/unsuspend.

Wiring:
- Admin badges on brief cards; actions reflect instantly.
```

---

## Prompt 8.2 — Reports and Blocks

```text
Goal: User reports and mutual blocks.

Requirements:
- Model `Report`; submit report for brief/user/message with reasons.
- Mutual block hides Apply and disables new messages; existing threads read-only.

Wiring:
- Add report entrypoints in UI menus; admin sees reporter note.
```

---

## Prompt 9.1 — Notifications (SES + In-app)

```text
Goal: Email + in-app notifications per spec.

Requirements:
- SES email transport; message batching (15m) for threads; immediate for applications.
- In-app notification center with read/unread.

Wiring:
- Test transport in dev; toggle via env for prod.
```

---

## Prompt 10.1 — Deploy & Analytics

```text
Goal: Configure AWS Amplify deploy, RDS Postgres, S3/CloudFront, GA4.

Requirements:
- Map env vars; provision DB and storage; run migrations in CI/CD.
- Hook GA4 measurement ID; respect privacy.

Wiring:
- Successful production deploy; smoke test endpoints.
```
