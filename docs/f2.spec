HatchCell Reverse VC – v1 Product Specification (Seller MVP)
Version: 2.0
Date: 2025-08-10

Overview
- Persona: founder/seller
- Primary flow (A): Draft → Validate → Publish listing → Receive offers/counters → Respond → Accept → KYC → Request payment → Buyer pays → e‑sign IP assignment → Payout → Handover
- Deal type: Offer/Counteroffer (full rights transfer)

Key Policies
- Currency: INR only; tax-inclusive (18% GST across all buyers)
- Pricing: Asking price + hidden minimum; custom step per listing; auto-counter snaps to nearest step to buyer’s offer but never below hidden_min; ask/hidden_min/offers are free-form (only auto-counter snaps)
- Offer transparency: Publicly show offer count + highest offer
- Reservation: Soft reserve; first to pay wins; auto-cancel the other
- Offers: Binding until seller acts; no auto-expiry; buyer cannot withdraw
- Buyer pay window: 48 hours starting when payment is requested (post-KYC)
- Seller KYC: Stripe Connect Express; must be completed within 24h of acceptance or acceptance auto-reverts
- Payout: After both e‑sign IP assignment; seller must countersign within 48h post-payment or auto-refund and reopen
- Refund policy: 7 days, seller-approval via ops
- NDA: Per-listing toggle; standard platform NDA (2-year term); auto-approve after accept; custom per-field gating
- Chat: Private 1:1 text-only, unlocked post-NDA
- Identity: Seller choice per listing (public real name or pseudonymous; school/org visibility optional)
- Moderation: Instant publish; post-review with ability to unlist; auto-flags + manual review within 48h; actions: warn, require edits (freeze), unlist, ban
- Contact sharing: Hard-block everywhere; auto-redact even post-NDA
- Listing freeze: Once first offer is received; new version required for changes; publishing new version auto-unlists old and redirects old → new
- Discovery: Public (no login) can view non-gated fields; SEO indexable with OG/Twitter; URL: /l/{slug}-{shortId}; default sort Most viewed; infinite scroll with “Load more” (20)

Required Fields to Publish (A–T)
- A Title (max 80)
- B One-line summary (max 170)
- C Detailed description (max 2000)
- D Problem statement (max 1000)
- E Target user/market (max 800)
- F Stage (Idea/MVP/Prototype/Launched/Revenue-generating)
- G Asking price (₹5,000–₹10,00,000; tax-inclusive)
- H Hidden minimum
- I Price step size (default ₹1,000; min ₹100; max ₹50,000)
- J Category (SaaS, Fintech, Edtech, Healthtech, eCommerce, AI/ML, Marketplace, DevTools, Consumer Apps, B2B Tools, Social/Community, Other)
- K Tags (free-form up to 5)
- L Required skills (hybrid: suggestions + allow new)
- M Attachments (images/PDF/ZIP; up to 20 files; 25 MB/file; 200 MB total)
- N Demo link (URL)
- O Validation evidence (hybrid: structured metrics + note + attachments; at least one metric required)
- P IP/Ownership status (original, assignable)
- Q NDA required toggle (plus per-field gating config)
- R Handover scope (checklist)
- S Handover timeline estimate (days)
- T Location (city/state)

Always Public (not gateable)
- Title, One-line summary, Problem statement, Stage, Category, Tags, Required skills

Validation Tools (A–G)
- Completeness checklist + readiness score
- Price guidance vs comps
- Content linting (lengths, clarity, banned words)
- Similar/duplicate detector
- IP attestation + third‑party asset disclosure
- Optional mentor review request (pre-publish)
- Post-publish auto-flags (risk signals)

Auto-Flag Signals (post-publish)
- Offensive/profane language in public fields
- Public fields contain contact info (email/phone/WhatsApp/handles)
- Mentions of off-platform payment or contact
- Price outlier vs category/stage
- Duplicate/similar listing text (high similarity)
- IP risk keywords (clone/copy/fork of X; “licensed assets” without disclosure)
- Suspicious attachments (malware scan fail; executables inside ZIP)
- Excessive external links (>3) in public fields
- NDA-gated fields still exposing sensitive data in public
- Repeated rapid edits (>5 in 10 mins) after publish
- Buyer/seller reported abuse
- Multiple accounts sharing same phone/device fingerprint

Handover Scope (Checklist)
- Code ZIP (source + dependencies list) [mandatory]
- README with setup/run instructions
- Architecture/technical docs
- Design source files (Figma/PSD)
- Product docs (feature list, roadmap)
- Sample/test data
- Demo assets (screenshots/video)
- Domain transfer
- Deployed hosting transfer (if any)
- Credentials handover (rotated; no API keys stored on platform)
- Third-party accounts/assets transfer (email, social, analytics)
- One handover call (30–60 mins)
- 7‑day bug-fix support window (in IP terms)
- License/OSS attribution summary
- Change log/version history
- Other (free-form)

Negotiation Rules
- Counters: Two-way, max 3 rounds per party; minimum increment = listing’s step
- Auto-counter: Applies to all proposals (initial and counters); snap to nearest step to buyer’s offer; never below hidden_min
- Multiple active proposals: Allowed; keep prior valid until explicitly declined; cap = 3 active per buyer per listing
- Acceptance with multiple proposals from same buyer: Disallow acceptance until seller declines other proposals from that buyer
- Seller may accept multiple buyers; first to pay wins; others auto-cancel
- Offers are binding until seller acts; buyers cannot withdraw; no auto-expiry
- Minimum offer threshold: Seller-defined % of asking; default 50%, min 50%, max 100%; rounded to nearest 1%

NDA and Access
- NDA per listing; platform standard; 2-year confidentiality term; custom per-field gating
- NDA auto-approve after accepting standard NDA
- Gated assets: preview-only for images/PDFs with visible watermark (buyer email/phone + timestamp); downloads disabled until payment; ZIPs blocked pre-payment
- Buyer verification for NDA auto-approval and offers:
  - India buyers: Phone OTP (AWS SNS) + basic profile (Full name, Verified email, Role, Organization/School, City/Country, Short intent note)
  - Non-India buyers: Google SSO + verified email + the same basic profile
- NDA required before offering: Seller toggle per listing (if off, offers still require above verification)
- Chat: Private 1:1 text-only; unlocked post-NDA

Payments, Fees, Taxes, Payouts
- Processor: Stripe
- Methods: UPI; Indian cards; International cards
- Merchant of Record: Platform; GST 18% to all buyers; tax-inclusive pricing with back-calculated GST shown at checkout
- Platform fee (seller pays; deducted from payout): tiered—15% ≤ ₹25k; 12% ₹25k–₹1L; 10% > ₹1L
- Stripe processing fees: paid by seller (deducted from payout)
- KYC: Stripe Connect Express required after acceptance but before requesting payment; 24h deadline or acceptance auto-reverts
- Payment window: 48h starts at payment request (post-KYC). Reservation is soft; first to pay wins
- IP assignment template: Standard Assignment + seller warrants ownership/non‑infringement; liability cap = sale price; 7‑day bug-fix handover; governing law India; arbitration under the Arbitration and Conciliation Act, 1996 (seat: Delhi)
- E‑sign: On-platform click-through (typed name + checkbox; capture timestamp/IP/UA; PDF generated)
  - Buyer signs during checkout (before payment)
  - Seller countersigns immediately after payment (deadline 48h; failure → auto-refund and reopen)
- Payout: After both e‑sign the IP assignment
- Refunds: 7-day window; only with seller approval via ops
- Code handover: Seller must upload a ZIP archive of the code; no GitHub transfer in v1

Offer and Listing State Machines
- Listing status (Minimal): Draft → Published → Reserved (accepted/payment requested/pending payment) → Sold → Unlisted
- Offer status (Simplified): Pending → Accepted → Payment Requested → Pending Payment → Paid → Declined → Auto‑canceled (other buyer paid or 48h elapsed) → Canceled by seller
- Freeze/versioning: Listing freezes on first offer; edits require a linked new listing; publishing new auto-unlists old and redirects old → new
- Unlisting: Prevent unlisting until all active offers are declined

Discovery & Marketplace
- Public can view non-gated fields; SEO indexable; OG/Twitter previews
- Public URL: /l/{slug}-{shortId}
- Default sort: Most viewed first
- Browse/search filters: Keyword search; Category; Stage; Price range; Sort by newest/price; NDA-required toggle; Required skills; Location; Demo link only; Verified seller badge
- Listing card content: Title; One-liner; Category chips; Stage; Asking price (INR, tax-inclusive label); NDA-required badge; Tags (top 3); Required skills; Seller identity snippet (per their choice); Location; Views count; Saves/Watchers count; Demo link badge; Verification badge; Version badge (if superseded)
- Saves/Watch: Yes; email + in-app updates (price/status/version)

Auth, Identity, Profile
- Auth: Auth.js (NextAuth) with Google SSO + email magic link (SES) + custom Phone OTP via AWS SNS
- ToS/Privacy: Required at first login (checkbox); marketing opt-in optional
- Age: 13+; same capabilities as adults
- Seller profile requirements to publish: Verified email, Phone OTP, Full name, School/Organization, City/Country, LinkedIn URL, Short bio (1–2 lines), Government/College ID upload (publish allowed after upload; Admin may later unlist if invalid)
- Limits: Max 3 active Published listings per seller

Notifications
- Channels: Email (SES) + in-app
- Triggers: NDA accepted; new chat message; offer received/counter/accepted/declined; payment requested; 24h/48h payment reminders; KYC reminders; version superseded; moderation actions; watcher updates
- Reminder cadences:
  - Seller KYC (24h deadline): Immediate, T−12h, T−1h
  - Buyer payment (48h window): Immediate, T−24h, T−4h, T−1h

Moderation, Abuse, Security
- Malware scanning: S3 + Lambda (ClamAV) on upload; quarantine on fail; block publish until clean
- Contact details: Hard-block in public fields and auto-redact in chat, even post-NDA
- Report/block: Enabled (preset reasons); block hides chat/offers between those users
- CAPTCHA: Enabled on NDA acceptance and offer submission (Provider: Cloudflare Turnstile)
- Rate limits:
  - NDA acceptances: 10 per buyer/day
  - Offers: 3 per buyer per listing/day; 10 per buyer/day global
  - Chat: 15 messages per conversation/min; 200 per buyer/day
  - Listing creation: 3 per seller/day

Analytics
- Public listing shows: offer count + highest offer
- Seller analytics dashboard: Views; Unique visitors; Saves/Watchers; NDA requests and acceptances; Chats started; Offer count; Highest offer; Average offer; Offer conversion rate (NDA→offer); Price change history; Traffic sources (referrers); Geo breakdown; Timeline of status changes; Moderation flags history; Validation score/checklist completion
- Product analytics: GA4 (events + basic funnels)

Infrastructure
- App: Next.js + API routes; hosted on AWS Amplify Hosting
- DB: PostgreSQL (AWS RDS, ap-south-1) + Prisma
- Storage/CDN: AWS S3 + CloudFront (signed URLs for gated previews/downloads)
- Emails: AWS SES (ap-south-1)
- SMS OTP: AWS SNS
- Region: ap-south-1 (Mumbai)
- Environments: Dev (dev branch) and Prod (main); PR previews OFF
- Monitoring: CloudWatch (logs/metrics/alarms)
- Alerting: SNS topic (email + SMS) with alarms:
  - API 5xx > 1% over 5m
  - Stripe webhook failures > 1 in 5m
  - SNS OTP error rate > 10% over 15m
  - AV scan failures > 1 in 10m
  - SES bounce rate > 5% over 1h
  - RDS CPU > 80% over 10m
  - S3 4xx/5xx > 1% over 15m
- Backups/retention:
  - RDS: 7-day PITR + 30-day weekly snapshots
  - S3: Versioning ON; noncurrent 30-day; Glacier 365-day

Data Model (high-level)
- users: id, email, google_id, phone, is_phone_verified, name, role, org_school, city, country, linkedin_url, intent_note, tos_accepted_at
- seller_profiles: user_id, bio, govt_id_url, govt_id_status, stripe_connect_account_id, connect_status
- listings: id, seller_id, title, one_liner, description, problem, target_market, stage, ask_amount, hidden_min, step_size, min_offer_percent, category, tags[], skills[], nda_required, gating_config, ip_status, handover_scope[], handover_timeline_days, location_city, location_state, status, is_frozen, previous_version_id, superseded_by_id, identity_visibility, views_count, saves_count, published_at
- listing_assets: id, listing_id, type (image/pdf/zip/demo_link), url, size_bytes, scan_status, preview_url, watermark_applied
- nda_acceptances: id, listing_id, buyer_id, accepted_at, ip, user_agent, verification_type
- chats: id, listing_id, buyer_id, seller_id, started_at
- messages: id, chat_id, sender_id, text, created_at, redaction_flags
- offers: id, listing_id, buyer_id, seller_id, amount, round_num_buyer, round_num_seller, created_at, status, accepted_at, payment_requested_at, payment_deadline_at, paid_at, declined_at, canceled_at, auto_canceled_reason
- transactions: id, offer_id, stripe_payment_intent_id, amount_total, gst_amount, platform_fee, stripe_fee, seller_payout_amount, payout_status
- ip_assignments: id, offer_id, buyer_signed_at, seller_signed_at, pdf_url, audit_metadata
- refunds: id, transaction_id, status, requested_at, approved_by_seller_at, processed_at
- moderation_flags: id, entity_type, entity_id, signal_type, created_at, status, actions
- watchers: id, listing_id, user_id, created_at
- reports: id, reporter_id, reported_user_id, reason, created_at, status
- blocks: id, blocker_id, blocked_user_id, created_at
- notifications: id, user_id, type, payload, read_at
- system_settings: fee_tiers, gst_rate, limits, captcha_enabled, etc.

API Endpoints (representative)
- Auth: /api/auth/* (NextAuth); /api/otp/request, /api/otp/verify
- Profile: GET/PUT /api/users/me; GET/PUT /api/seller-profile
- Listings:
  - POST /api/listings (create draft)
  - PUT /api/listings/{id} (edit; blocked if frozen)
  - POST /api/listings/{id}/publish
  - POST /api/listings/{id}/unlist (blocked if active offers)
  - POST /api/listings/{id}/version (create new, link, auto-unlist old)
  - GET /api/listings (browse/search with filters, sort, pagination)
  - GET /api/listings/{slugId} (public details with gating)
- Assets:
  - POST /api/listings/{id}/assets/sign-upload
  - POST /api/assets/{id}/scan-callback
  - GET /api/assets/{id}/preview (signed)
- NDA:
  - POST /api/listings/{id}/nda/accept (with CAPTCHA)
  - GET /api/listings/{id}/gated-fields
- Chat:
  - POST /api/listings/{id}/chats (post-NDA)
  - GET/POST /api/chats/{id}/messages (rate-limited; redaction)
- Offers:
  - POST /api/listings/{id}/offers (with CAPTCHA; enforce min% if set)
  - POST /api/offers/{id}/counter (step rules, round caps)
  - POST /api/offers/{id}/accept (block if other active from same buyer)
  - POST /api/offers/{id}/decline
  - POST /api/offers/{id}/request-payment (requires seller KYC)
- Payments:
  - POST /api/payments/{offerId}/checkout (buyer e‑sign during checkout)
  - POST /api/stripe/webhook
- IP Assignment:
  - POST /api/ip/{offerId}/buyer-sign
  - POST /api/ip/{offerId}/seller-sign
- Watch:
  - POST/DELETE /api/listings/{id}/watch
- Analytics:
  - GET /api/seller/listings/{id}/analytics
- Admin:
  - Flags, actions, unlist, ban; view IDs; payouts/refunds ops

Acceptance Criteria (selected)
- Listing publish is blocked until A–T pass; malware scans complete; seller profile A–H satisfied
- Gated assets show watermarked previews; downloads disabled pre-payment; ZIPs blocked pre-payment
- NDA auto-approval applies after verification; chat unlocks only post-NDA
- Offers respect step auto-counter rules; round caps; multiple active proposals rules; acceptance blocking for same-buyer multiples
- Acceptance triggers 24h KYC deadline; if missed, auto-revert acceptance and notify both parties
- Payment request starts 48h timer; reminder emails schedule as specified
- Buyer signs IP assignment at checkout; post-payment, seller must countersign within 48h or auto-refund and reopen; payout only after both signatures
- Public listing shows offer count + highest offer; SEO indexable; OG/Twitter previews render public fields only
- Marketplace browse supports filters; default sort Most viewed; infinite scroll with load more (20)
- Rate limits enforced; CAPTCHA on NDA acceptance and offer submission
- CloudWatch alarms via SNS (email+SMS) per thresholds; backups/retention configured

CAPTCHA Provider
- Cloudflare Turnstile
