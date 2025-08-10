# UI Task Checklist (MVP user-visible steps)

Each task is small and user-testable in the UI. For each, we list how to check, expected current changes, and future work to defer.

---

## 0.1 Foundations

- Path to check: `/`, `/briefs`, `/briefs/some-slug`, `/auth/signin`
- Steps to validate:
  - Navigate via top nav; pages render placeholders.
- Expected now:
  - Basic layout, nav, Tailwind styling working.
- Future:
  - shadcn/ui components; polished theming and tokens.

## 1.1 Sign in with Google/Email

- Path to check: `/auth/signin`
- Steps to validate:
  - Click provider, complete flow, see user menu in nav.
- Expected now:
  - Session persists; sign out works.
- Future:
  - Account menu polish, error states, loading skeletons.

## 1.2 Minimal Profiles

- Path to check: `/profile`
- Steps to validate:
  - Complete required fields; attempting to post/apply without profile redirects here.
- Expected now:
  - Save profile; guard flows.
- Future:
  - Multi-step wizard UX; validation hints.

## 2.2 Create Draft Brief

- Path to check: `/briefs/new`
- Steps to validate:
  - Fill required fields; save creates Draft; redirect to detail.
- Expected now:
  - Draft badge visible to owner; persisted fields show.
- Future:
  - Autosave; multi-step wizard; client-side schema validation.

## 2.3 Publish/Unlist Brief

- Path to check: owner brief detail
- Steps to validate:
  - Publish makes it publicly visible; unlist hides from listing.
- Expected now:
  - Applications toggle defaults Open on publish.
- Future:
  - OTP requirement gating publish.

## 3.1 Briefs Listing

- Path to check: `/briefs`
- Steps to validate:
  - Published briefs render as cards; pagination works.
- Expected now:
  - Latest sort default.
- Future:
  - Infinite scroll.

## 3.2 Filters and Search

- Path to check: `/briefs`
- Steps to validate:
  - Apply filters and keyword search; URL updates; results change.
- Expected now:
  - Filters impact query.
- Future:
  - Postgres ILIKE; more facets; saved filters.

## 3.3 Most Active Sort

- Path to check: `/briefs`
- Steps to validate:
  - Switch sort to Most active; order reflects activity.
- Expected now:
  - Tie-break by publish date.
- Future:
  - Activity badges on cards.

## 4.1 Apply to Brief

- Path to check: brief detail (as applicant)
- Steps to validate:
  - Submit application; resubmit updates; withdraw then re-apply.
- Expected now:
  - Founder sees application in owner view.
- Future:
  - Rate limits and rich validations.

## 4.2 Application Messaging

- Path to check: application thread UI
- Steps to validate:
  - Send/receive text messages; see updates via 10s polling.
- Expected now:
  - Thread created on first application.
- Future:
  - Typing indicators; read receipts; websockets.

## 5.1 Project Created on Accept

- Path to check: `/projects/{id}`
- Steps to validate:
  - Accept application; redirected to project Overview.
- Expected now:
  - Participants listed; summary visible.
- Future:
  - Undo window UI and timers.

## 5.2 Milestones CRUD

- Path to check: project Milestones tab
- Steps to validate:
  - Create/edit milestones; update status; manage checklist.
- Expected now:
  - Permissions enforced for founder/co-builder.
- Future:
  - Reorder milestones; due reminders.

## 6.1 File Uploads (Local)

- Path to check: application form and brief assets
- Steps to validate:
  - Attach PDF resume; attach images/PDF assets; validations enforced.
- Expected now:
  - Local storage adapter; preview links work.
- Future:
  - Progress bars; drag and drop.

## 6.2 S3 Uploads (Presigned)

- Path to check: same as 6.1
- Steps to validate:
  - Uploads succeed to S3; public reads via CloudFront.
- Expected now:
  - No UI change; only backend adapter swap.
- Future:
  - Asset management and delete confirmations.

## 7.1 OTP (Stub)

- Path to check: profile phone verification
- Steps to validate:
  - Request and verify code; publish/apply gated until verified.
- Expected now:
  - Verified state shown in profile.
- Future:
  - SMS provider, resend timers, lockouts.

## 7.2 OTP via SNS + Limits

- Path to check: same as 7.1
- Steps to validate:
  - Codes delivered via SMS; excessive requests blocked per limits.
- Expected now:
  - India-only restriction enforced.
- Future:
  - Better error UI and retry UX.

## 7.3 Rate Limits (Apply/Messaging)

- Path to check: applying and sending many messages
- Steps to validate:
  - Exceed limits → see errors; UI disables temporarily.
- Expected now:
  - 429s with remaining quota headers.
- Future:
  - User-visible counters and cooldown timers.

## 8.1 Admin & Moderation

- Path to check: `/admin`, `/admin/review`
- Steps to validate:
  - Admin-only access; perform takedown/restore and feature/unfeature.
- Expected now:
  - Actions reflect immediately in lists and detail.
- Future:
  - Audit logs; bulk actions.

## 8.2 Reports and Blocks

- Path to check: report menus, messaging/apply
- Steps to validate:
  - Submit report; blocked users cannot start new messages or apply.
- Expected now:
  - Existing threads become read-only.
- Future:
  - Report triage UX; attachments in reports.

## 9.1 Notifications

- Path to check: application submissions and messages
- Steps to validate:
  - Emails sent for applications; message emails batched; in-app badges.
- Expected now:
  - Test transport used in dev.
- Future:
  - Digest settings; per-thread mute.

## 10.1 Deploy & Analytics

- Path to check: production site
- Steps to validate:
  - Successful deploy; GA4 events visible; basic smoke tests pass.
- Expected now:
  - Environment variables correctly wired.
- Future:
  - Observability dashboards and alerts.
