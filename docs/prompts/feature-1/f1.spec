# HatchCell F1 Spec — Co-build MVPs (v1)

This document consolidates all decisions for HatchCell v1 (Feature 1: Find Co‑founder / Co‑build MVPs) into a developer‑ready specification.

## 1. Product Overview

- Goal: Enable founders to post co‑build MVP briefs and collaborate with a single accepted co‑builder through applications, messaging, and a lightweight project workspace with milestones.
- Primary personas:
  - Founder: posts a brief, reviews applications, accepts one co‑builder, manages project/milestones.
  - Student/Co‑builder: discovers briefs, applies, collaborates in project workspace.

## 2. Architecture & Infra

- App: Next.js (App Router), deployed on AWS Amplify.
- DB: Postgres (AWS RDS) with Prisma ORM.
- Auth: Auth.js (NextAuth) using stateless JWT sessions (7‑day rolling); providers: Google SSO + Email magic link; custom phone OTP via AWS SNS (India‑only).
- Storage & CDN: S3 for uploads with presigned URLs; CloudFront for delivery.
- Email/SMS: SES (email), SNS (SMS). SMS sender ID configured for India.
- Analytics: GA4 only for traffic/visitor metrics; no per‑view events stored in DB for v1.
- Region: ap‑south‑1.

## 3. Environment Configuration (Amplify env vars)

- AUTH: `NEXTAUTH_URL`, `NEXTAUTH_SECRET`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `EMAIL_FROM`, `EMAIL_SERVER` (SES SMTP URL)
- DB/ORM: `DATABASE_URL`
- AWS core: `AWS_REGION=ap-south-1`, `AWS_S3_BUCKET`, `CLOUDFRONT_URL`
- SMS OTP:
  - `SNS_SENDER_ID`
  - `OTP_MAX_REQ_PER_HOUR=3`
  - `OTP_MAX_REQ_PER_DAY=6`
  - `OTP_MAX_ATTEMPTS=5`
  - `OTP_LOCK_MINUTES=15`
  - `OTP_INDIA_ONLY=true`
- App: `APP_URL`, `ADMIN_EMAIL_WHITELIST` (comma‑separated)
- Analytics: `GA4_MEASUREMENT_ID`

## 4. Branding & UI

- Brand name: HatchCell.
- UI stack: Tailwind CSS + shadcn/ui.
- Wordmark: text “HatchCell” with Inter font; no logo asset v1.
- Color palette (primary cyan/teal provided; see design tokens in app).

## 5. Routing / Pages

- Public: `/`, `/briefs`, `/briefs/[slugId]` where `[slugId] = {slug}-{shortId}`
  - Slug: lowercase hyphenated title, max 60 chars.
  - shortId: 8‑char base62.
- Founder: `/briefs/new`, `/founder/briefs`, `/messages`, `/messages/[id]`, `/profile`
- Admin: `/admin`, `/admin/review`
- Auth: `/auth/signin`
- Project workspace (participants only): `/projects/[id]` with tabs `overview`, `milestones`, `messages`

Homepage `/`: Hero + primary CTA “Post a brief”, secondary “Browse briefs”, grid of briefs (default sort Latest).

## 6. Authentication & User Accounts

- Sign‑in required to start posting a brief and to apply.
- Providers: Google SSO, Email magic link (Auth.js).
- Sessions: stateless JWT, 7‑day rolling.
- ToS/Privacy: required consent checkbox at first login; marketing opt‑in optional.
- Phone OTP verification:
  - Founders: required at publish time.
  - Applicants: required before applying.
  - India‑only (+91). Limits: 3 requests/hour, 6/day, 5 attempts/code, lock for 15 min after 5 failures.
- Admin access: email whitelist via `ADMIN_EMAIL_WHITELIST`.

### Minimal Profiles (required before post/apply)

- Founder (required unless noted): Name, Title/Role, Contact email, Phone (OTP verified), Location/Timezone; optional: Organization, Short bio.
- Student (required unless noted): Name, Skills (tags), GitHub/Portfolio, Availability, Location/Timezone; optional: Education/Experience level, Short bio.

## 7. Briefs

### Schema (fields)

- Title (req, ≤80)
- Problem statement (req, ≤600)
- Goals / success criteria (req, ≤400)
- Key features (req: 3–5 items; each ≤120 chars)
- Out of scope (opt, ≤400)
- Target users (req, ≤300)
- Preferred experience level (req; enum: Beginner | Intermediate | Advanced)
- Required skills (req, 1–8 tags; hybrid taxonomy: suggest from list + allow new)
- Compensation (opt; enum: Paid | Open | Equity). If Paid → optional INR min/max.
- Timeline (req; start date; duration 1–52 weeks)
- Preferred availability (req; hours/week min–max; earliest start date)
- Preferred location/timezone (req)
- Deliverables (req, ≤500)
- Assets provided (opt, ≤300; e.g., APIs/designs/datasets)
- Constraints (opt, ≤300; tech/legal/IP)
- Contact method (fixed: in‑app Apply)
- Visibility (req; Public by default; optional private‑link toggle → noindex)
- Applications toggle (Open/Closed; defaults Open on publish)

Notes:
- Contact details are allowed in free‑text fields and messages (no redaction).
- Public briefs are SEO indexable with OG/Twitter metadata; private‑link briefs are excluded from listings/search and set `noindex`.

### File Uploads

- Resumes/CV: PDF only, max 10 MB.
- Brief assets: PNG/JPG/PDF, up to 10 files, max 10 MB each, 50 MB total.
- Uploads via presigned S3 URLs; served via CloudFront.

### Status Machine & Moderation

- Draft → Publish → Published.
- Published → Unlist (by founder) → Unlisted → Re‑publish → Published.
- Published/Unlisted → Remove (by admin) → Removed.
- Delete allowed only in Draft/Unlisted.
- Publishing: immediate live with post‑review; edits go live instantly (post‑review applies).
- Admin actions: review queue, takedown/restore, feature/unfeature, suspend/unsuspend user.

### Rate Limits

- Brief creation: 3 per user per day.

## 8. Brief Discovery

- Public listing at `/briefs` with infinite scroll (batch size 12).
- Filters (all live together):
  - Required skills
  - Timeline/duration
  - Compensation (Paid/Open/Equity)
  - Availability (hours/week, start date)
  - Experience level
  - Location/timezone
- Keyword search: Postgres ILIKE across Title, Problem statement, Key features, Required skills, Deliverables, Target users.
- Default sort on listing: Most active within last 7 days with equal weight score = `2 × applications + 1 × messages` (computed on query). Homepage grid defaults to Latest.

## 9. Applications

- Auth: sign‑in required; ToS/Privacy accepted; minimal profile complete; phone OTP verified.
- Apply form:
  - Required: Cover message; Relevant skills (select from brief + add custom); Availability (hours/week, start date); GitHub/portfolio link.
  - Optional: Resume/CV (upload or link); LinkedIn; Location/timezone; Expected compensation; Extra notes/questions.
- One active application per user per brief. Further submissions update existing application. Applicant may Withdraw then re‑apply.
- Status flow: Pending → Accepted | Rejected | Withdrawn (by applicant).
  - Founder actions: Accept, Reject, Undo within 24h.
  - Notifications on all state changes (both parties).
- Messaging: 1:1 thread auto‑created on application; basic text only; polling every 10 seconds; rate limits enforced.
- Notifications:
  - New application → founder notified: email + in‑app, immediate per application.
  - New message → recipient notified: email + in‑app, batched with 15‑minute throttle.
- Rate limits:
  - Apply: 3 applications per user per brief per day; 10 applications per user per day (global).
  - Messaging: 10 messages per thread per minute; 100 messages per user per day.
- CAPTCHA: none in v1.

### Save/Watch

- Signed‑in users can Save/Watch briefs.
- Notifications: in‑app on significant brief updates (edits, applications reopened). Email may be added later.

## 10. Project Workspace (post‑Accept)

- Creation: When a founder Accepts an application, a single project is created (v1: single co‑builder per brief).
- Participants: Founder, accepted Co‑builder, invited Mentors (email) with view + comment only; Admins have access.
- Privacy: visible only to participants and admins.
- Tabs: Minimal — Overview, Milestones, Messages.
- Threading: Start a new project‑level Messages thread on Accept (separate from application thread).

### Overview tab

- Project summary: Title, Problem statement, Goals/success criteria.
- Key info: Estimated completion date, optional Agreement note (amount/scope/date if provided), Project status (Active/On hold/Completed).
- Participants: Founder, Co‑builder, Mentors.
- Links: Repo URL, Live site, Docs (optional).
- Next up: Next milestone (nearest due or In progress).

### Milestones

- Default template (editable; add/edit/remove allowed):
  1) Name decided + brand palette
  2) Domain purchased + DNS set
  3) Company registration (if applicable)
  4) Problem statement finalized
  5) Market research + insights
  6) Target users/personas
  7) Competitive landscape
  8) Solution outline + success criteria
  9) MVP scope (features in/out)
  10) Tech stack + repo setup
  11) Landing website live
  12) Prototype/MVP build
  13) User testing + feedback
  14) Pitch deck ready
  15) Funding applications submitted
  16) Legal/IP and compliance
  17) Go‑to‑market plan
  18) Estimated completion date
  19) Founder/co‑founder details finalized
  20) Mentor review sessions

- Milestone schema:
  - Required: Title; Status (Not started | In progress | Blocked | Done)
  - Optional: Description; Due date; Owner (founder or co‑builder); Checklist (0–20 items); Attachments (files/links); Comments (thread); Progress percent (0–100)

### Permissions & Notifications

- Edit permissions: Founder + Co‑builder can create/edit milestones and update Overview.
- Project status: Founder + Co‑builder can set; Completed does not lock milestones.
- Notifications: In‑app only for milestone status changes and 24‑hour due reminders.

### Agreement (payments skipped)

- On Accept: optional Agreement note (free text: amount/currency, scope/milestone, expected delivery date). No in‑app payments in v1.

## 11. Admin & Moderation

- Dashboard: `/admin`, `/admin/review`.
- Actions: review queue (flagged/new briefs), takedown/restore brief, feature/unfeature brief, suspend/unsuspend user.
- Reports/Blocks (v1 enabled):
  - Report reasons: Spam, Harassment, Inappropriate content, Off‑platform solicitation, IP infringement, Other (free‑text).
  - Scope: report a brief, a user, or a specific message.
  - Block: mutual; hides Apply and disables new messages; existing threads read‑only; either party can unblock.
  - Admin sees reporter note/screenshot in review queue.

## 12. API Design (Route Handlers under `app/api/*`)

- Auth & OTP
  - `POST /api/auth/[...nextauth]` — Auth.js providers (Google, Email); JWT strategy
  - `POST /api/otp/request` — request phone OTP (India‑only; enforce limits)
  - `POST /api/otp/verify` — verify code; attach to user phone

- Briefs
  - `GET /api/briefs` — list with filters, search (ILIKE), sort, pagination (infinite scroll, `limit=12`, `cursor`)
  - `POST /api/briefs` — create Draft (auth required)
  - `GET /api/briefs/{id}` — fetch detail
  - `PATCH /api/briefs/{id}` — edit (auth + owner)
  - `POST /api/briefs/{id}/publish` — requires phone OTP verified
  - `POST /api/briefs/{id}/unlist` / `POST /api/briefs/{id}/republish`
  - `POST /api/briefs/{id}/applications-toggle` — Open/Closed
  - `POST /api/briefs/{id}/feature` (admin) / `POST /api/briefs/{id}/remove` (admin)

- Applications & Messaging
  - `POST /api/applications` — apply (enforce one active; rate limits; create app thread)
  - `GET /api/applications` — list (owner founder; or applicant’s own)
  - `PATCH /api/applications/{id}` — status changes (Accept/Reject/Undo/Withdraw)
  - `GET /api/messages/threads` — list user threads (app + project)
  - `GET /api/messages/threads/{id}` — get messages (polling)
  - `POST /api/messages/threads/{id}` — send message (rate limits)

- Projects & Milestones
  - `POST /api/projects` — created internally on Accept
  - `GET /api/projects/{id}` — detail (participants/admin only)
  - `PATCH /api/projects/{id}` — update overview/status/links
  - `GET /api/projects/{id}/milestones` — list
  - `POST /api/projects/{id}/milestones` — create
  - `PATCH /api/projects/{id}/milestones/{mid}` — update
  - `DELETE /api/projects/{id}/milestones/{mid}` — remove

- Saves/Watch & Reports
  - `POST /api/briefs/{id}/save` / `DELETE /api/briefs/{id}/save`
  - `GET /api/saves` — current user’s saved briefs
  - `POST /api/reports` — submit report (brief/user/message)

## 13. Data Model (conceptual)

- User: id, name, email, phone, roles (founder/student), timezone, createdAt/updatedAt, suspendedFlag
- ProfileFounder: userId (1‑1), title, organization?, bio?, locationTimezone
- ProfileStudent: userId (1‑1), skills (denormalized text for quick search), portfolio, availability, locationTimezone, educationLevel?, bio?
- Brief: id, ownerUserId, slug, shortId, title, problem, goals, keyFeatures[], outOfScope?, targetUsers, preferredExperienceLevel, requiredSkills[], compensationType, compMin?, compMax?, startDate, durationWeeks, preferredAvailability(minHours,maxHours,earliestStartDate), preferredLocationTimezone, deliverables, assetsProvided?, constraints?, visibility(public/privateLink), applicationsOpen(bool), status(enum Draft/Published/Unlisted/Removed), featured(bool), publishedAt, updatedAt
- Skill (controlled list): id, name, slug; plus freeTag string values attached on Brief/Application to support hybrid
- Application: id, briefId, applicantUserId, status(enum Pending/Accepted/Rejected/Withdrawn), coverMessage, relevantSkills[], availability, portfolioLink, resumeUrl?, linkedin?, locationTimezone?, expectedComp?, extraNotes?, createdAt, updatedAt, statusChangedAt, undoDeadlineAt
- MessageThread: id, type(enum Application|Project), briefId?, applicationId?, projectId?, participantIds[], createdAt
- Message: id, threadId, senderUserId, body, createdAt
- Project: id, briefId, founderUserId, coBuilderUserId, status(enum Active/OnHold/Completed), estimatedCompletionDate?, agreementNote?, repoUrl?, liveUrl?, docsUrl?, createdAt, updatedAt
- ProjectParticipant: projectId, userId, role(enum Founder|CoBuilder|Mentor), permissions (view/comment/edit flags)
- Milestone: id, projectId, title, status(enum NotStarted|InProgress|Blocked|Done), description?, dueDate?, ownerUserId?, progressPercent?, createdAt, updatedAt
- MilestoneChecklistItem: id, milestoneId, text, done(bool), order
- Save: userId, briefId, createdAt
- Report: id, reporterUserId, targetType(enum Brief|User|Message), targetId, reason(enum), note?, screenshotUrl?, createdAt, resolvedByAdminId?, resolvedAt?
- OTP: id, userId, phoneE164, codeHash, expiresAt, attempts, lockedUntil, createdAt
- RateLimitEvent: id, userId, scope(enum Apply|Message|BriefCreate|OTPRequest|OTPVerify), key, createdAt (used for counting windows)

Note: “Most active” is computed on query using counts from Applications and Messages within last 7 days; no stored `activity_score`.

## 14. Validation Rules

- See field limits in Briefs schema above.
- Slug normalization: lowercase, alphanumerics + hyphens, collapse duplicates, trim to 60 chars.
- shortId: 8‑char base62 unique.
- Upload validations: types/sizes as specified.
- Enum values enforced per fields.

## 15. Listing: Pagination & Sorting

- Pagination: infinite scroll with cursor (createdAt DESC for Latest; for Most active, sort by computed score, tie‑break by publish date DESC).
- Batch size: 12.

## 16. Notifications

- Applications: founder receives email + in‑app immediately per new application; applicant receives confirmation.
- Messages: recipient receives email + in‑app, batched with 15‑minute throttle.
- Project workspace: in‑app only for milestone status changes and 24‑hour due reminders.
- Saves/Watch: in‑app notifications on significant brief updates (edits, applications reopened).

## 17. Security & Privacy

- Access control:
  - Brief edit/publish/unlist: owner only; admin moderation allowed.
  - Applications visibility: founder sees applications to their briefs; applicant sees their own.
  - Messages: participants of the thread only.
  - Project workspace: participants (founder, co‑builder, mentors) and admins only.
- CAPTCHA: none in v1.
- Contact details allowed in brief fields and messages.

## 18. SEO & Metadata

- Public briefs: indexable; generate OG/Twitter cards (title, summary, image if any).
- Private‑link briefs: excluded from listings/search and set `noindex`.

## 19. Acceptance Criteria

### A. Founder posts a brief

- Auth required (Google/email); ToS/Privacy accepted; minimal founder profile complete.
- Phone OTP verified at publish.
- Multi‑step wizard with autosave; inline validation per limits.
- Required fields present including Preferred experience level, Preferred availability, Preferred location/timezone.
- On Publish: brief live immediately; Applications toggle defaults Open.
- Public page at `/briefs/{slug}-{shortId}` (8‑char base62); SEO+OG/Twitter enabled when public.
- Brief appears in public list; filters and keyword search working; homepage shows Latest.
- Notifications: founder gets email + in‑app on each new application (immediate).
- Edits to published brief go live instantly; changes visible in list and detail.
- Admin can unlist/remove; post‑review moderation active.

### B. Student applies to a brief

- Sign‑in required; ToS/Privacy accepted; minimal student profile complete; phone OTP verified.
- Apply form validates required fields; hybrid skills select+add; resume optional (PDF ≤10 MB).
- One active application per brief; subsequent submission updates; applicant can Withdraw and re‑apply.
- On submit: founder notified via email + in‑app immediately; applicant gets confirmation.
- Status flow: Pending → Accepted | Rejected | Withdrawn; founder can Undo within 24h; notifications on all changes.
- Messaging: thread auto‑created; polling every 10s; rate limits enforced.
- “Most active” score updates based on new app/message (computed on query at listing time).

### C. Project workspace

- On Accept: creates project (single co‑builder). New project‑level thread starts.
- Tabs: Overview, Milestones, Messages.
- Permissions: Founder + Co‑builder can edit Overview & Milestones; Mentors view/comment.
- Project status editable by Founder + Co‑builder; Completed does not lock milestones.
- Notifications: in‑app only for milestone changes and due reminders.
- Privacy: only participants and admins can view.


