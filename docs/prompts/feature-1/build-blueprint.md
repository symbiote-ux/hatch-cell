# HatchCell F1 Build Blueprint (Developer Plan)

This blueprint translates the F1 Spec into an incremental, testable build plan with small steps that always keep the app running. Each step ends with clear acceptance criteria and user‑visible outcomes (where applicable).

Guiding principles:

- Start local-first (SQLite, stubs), add AWS integrations later.
- Ship thin vertical slices that can be exercised in the UI after each step.
- Keep auth, data models, and routes minimal at first; expand under feature flags.

## Phase 0 — Foundations

0.1 Baseline UI/UX stack and routing skeleton

- App Router layout, navigation, Tailwind ready, shadcn/ui setup later.
- Pages: `/`, `/briefs`, `/briefs/[slugId]`, `/auth/signin` (placeholder), dashboard stubs.
  Acceptance:
- App builds and routes render without runtime errors.

  0.2 Type-safe tooling

- ESLint, TypeScript strict enough for safety, basic CI-ready scripts.
  Acceptance:
- `npm run lint` passes; typecheck clean.

## Phase 1 — Auth and Accounts (local-first)

1.1 Auth.js with Google + Email (magic link) using JWT sessions

- Local dev uses `.env.local`; production vars deferred.
- Minimal `User` table via Prisma; link sessions through JWT callbacks.
  Acceptance:
- User can sign in/out; session available in server components and API.

  1.2 Minimal profiles

- `ProfileFounder`, `ProfileStudent` 1‑1 tables; guard post/apply flows on minimal completeness.
  Acceptance:
- If profile incomplete, redirects to `/profile` wizard stub.

## Phase 2 — Briefs MVP

2.1 DB and models

- Prisma schema for `Brief`, `Skill` (controlled list), hybrid `requiredSkills`.
  Acceptance:
- `prisma migrate dev` creates schema; seed adds sample skills.

  2.2 Create/Edit Draft Brief

- Multi-step wizard (thin); autosave later; validation per spec limits.
  Acceptance:
- Authenticated founder can create a Draft via `/briefs/new`; data persists.

  2.3 Publish/Unlist lifecycle (without OTP yet)

- Status transitions Draft ↔ Published ↔ Unlisted; Applications default Open.
  Acceptance:
- Publish makes brief visible at `/briefs/{slug}-{shortId}` and on `/briefs` (Latest).

## Phase 3 — Discovery

3.1 Public listing `/briefs` (infinite scroll later)

- Server-rendered list; simple pagination first, switch to cursor later.
  Acceptance:
- Lists Published briefs; clicking opens detail.

  3.2 Filters + Keyword search

- Required skills, experience, compensation, duration, availability, timezone; Postgres ILIKE search later (fallback contains for SQLite).
  Acceptance:
- Filters affect results; query params persist state.

  3.3 “Most active” sort (computed on query)

- Compute using Applications/Messages counts in last 7 days; tie-break by publish date.
  Acceptance:
- Sort option toggles between Latest and Most active.

## Phase 4 — Applications and Messaging

4.1 Apply flow

- Single active application per user per brief; update on resubmit; withdraw.
  Acceptance:
- Applicant can submit/withdraw; founder sees application list on their brief.

  4.2 Application thread (text-only)

- 1:1 thread created on first application; polling every 10s; rate limits later.
  Acceptance:
- Both parties can exchange messages in the app thread; polling updates.

## Phase 5 — Projects & Milestones

5.1 Project creation on Accept

- Accept turns application into `Project` with participants; project-level thread created.
  Acceptance:
- On Accept, `/projects/{id}` renders Overview with participants.

  5.2 Milestones MVP

- CRUD milestones; statuses; optional fields; checklist items.
  Acceptance:
- Participants can add/edit milestones; status changes persist.

## Phase 6 — Files & Uploads

6.1 Local stub uploads

- Local adapter (in-memory or /tmp) for Resume/Assets; validations as per spec.
  Acceptance:
- Can attach PDF to application; validations enforced.

  6.2 S3 presigned upload + CloudFront read

- Swap adapter to S3; presigned PUT; public read via CloudFront URL config.
  Acceptance:
- File uploads succeed to S3 in dev/prod with correct size/type limits.

## Phase 7 — OTP (Phone) and Rate Limiting

7.1 OTP flow (stub)

- Request/Verify endpoints with local code generator; attach phone to user.
  Acceptance:
- Flows block publish/apply until verified (founder/applicant rules).

  7.2 SNS integration + limits

- Enforce per-hour/day request limits; attempts; lockouts; India-only.
  Acceptance:
- SMS sent via SNS in `ap-south-1`; limits enforced; audit trail events recorded.

  7.3 Rate limits for apply/messaging/global caps

- Implement windowed counters using `RateLimitEvent`.
  Acceptance:
- Exceeding limits yields 429; counters reset per window.

## Phase 8 — Admin & Moderation

8.1 Admin dashboard and actions

- Review queue, takedown/restore, feature/unfeature, suspend/unsuspend.
  Acceptance:
- Admin email whitelist gates access; actions persist and reflect in UI.

  8.2 Reports/Blocks

- Submit report (brief/user/message); mutual blocks affect UI and APIs.
  Acceptance:
- Blocking hides Apply and disables new messages in affected threads.

## Phase 9 — Notifications

9.1 Email (SES) and in-app

- Immediate app submit emails; 15-min batched message emails; in-app toasts/badges.
  Acceptance:
- Emails delivered in dev via test transport; prod via SES; batching respected.

## Phase 10 — Deployment & Ops

10.1 Amplify config + envs

- Map all env vars; region `ap-south-1`; RDS & S3 credentials; CloudFront URL.
  Acceptance:
- Production deploy green; health checks pass; basic analytics GA4 wired.

---

Deliverables per step:

- Code edits, route handlers (`app/api/*`), pages, Prisma migrations, and docs updates.
- Each step has a companion prompt (see `docs/prompts/implementation-prompts.md`) and a UI checklist (`docs/tasks/ui/tasks.md`).
