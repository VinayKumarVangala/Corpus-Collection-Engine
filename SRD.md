# Security Requirements

**Project:** Corpus Collection Engine – Preserving Indian Culture & Diversity  
**Scope:** Streamlit application (Hugging Face Spaces) with optional FastAPI/Flask backend; DB (Firebase Firestore or MongoDB Atlas); object storage (Firebase Storage/IPFS/Cloudinary); offline-first sync; multi-category, multi‑media (Text/Image/Audio/Video) corpus collection; user dashboard.  
**Goal:** Protect users, content, and infrastructure while enabling low‑bandwidth/offline contributions; comply with open-source, privacy, and cultural sensitivity expectations.

---

## 1) Assumptions & Trust Boundaries
- **Clients:** Web browsers (mobile/desktop), possibly PWA for offline cache. Untrusted.  
- **Edge:** Hugging Face Spaces (public) hosting Streamlit UI; optional backend API endpoint(s).  
- **Services:** Firestore / MongoDB Atlas (DB), Firebase Storage / Cloudinary / IPFS (media).  
- **Data Types:** (a) Account & profile (PII-lite), (b) Contribution metadata, (c) Media files, (d) Analytics/telemetry, (e) Access tokens/refresh tokens.  
- **Threats:** Account takeover, abusive uploads (malware/illegal content), spam, scraping, model poisoning, sensitive data leakage, supply-chain dependency risks, misconfig of cloud rules, token theft, offline cache exposure.

---

## 2) Roles & Access Model
- **Anonymous Visitor:** Browse public info and ToS/Policy. No upload.  
- **Authenticated Contributor:** Create, view own contributions, edit/delete own, view personal dashboard.  
- **Moderator:** Review/approve/label, remove/restore, handle abuse reports.  
- **Admin:** Configure categories, storage policies, keys/secrets; full audit access.  
- **Principles:** Least privilege, role-based authorization (RBAC), deny-by-default.

---

## 3) Data Classification & Handling
- **Class A – Account/PII-lite:** email, display name, language. _Confidential_.  
- **Class B – Contribution Metadata:** titles, tags, geo-region (optional & coarse), language, category. _Internal by default; public subset_.  
- **Class C – Media:** text/image/audio/video uploads. _Public by default only with explicit user consent_; otherwise _Internal_.  
- **Class D – Security Artifacts:** tokens, API keys, logs. _Highly Confidential_.  
- **Controls:** Minimize PII; clear consent on visibility/licensing; allow pseudonyms; expose only necessary public fields.

---

## 4) Authentication Requirements (Strong Auth)
**Core**  
- **Password-based auth** (if used):
  - Store with **Argon2id** (time/mem hardening; >= 64MB memory, calibrated iterations).  
  - Password policy: min 12 chars; check against breached lists (k‑anonymity).  
  - Throttle by IP + account, exponential backoff; lockout window (e.g., 10 fails → 15 min).  
- **Passkeys (WebAuthn)**: Offer as primary or 2FA for phishing‑resistant auth.  
- **TOTP 2FA**: Optional when passkeys not available; backup codes.  
- **OAuth2 social (optional)**: Only providers supporting email verification; still bind to local RBAC.

**Sessions & Tokens**  
- **JWT access tokens**: Short TTL (≤ 15 min); **aud/iss** claims; rotate signing keys; sign with ES256/RS256.  
- **Refresh tokens**: httpOnly, Secure cookies (SameSite=Lax/Strict) or encrypted local storage via WebCrypto; rotation & reuse detection.  
- **CSRF**: If cookie-based, use SameSite + CSRF token; else use Authorization header with Bearer tokens.  
- **Device binding**: Store token fingerprint (hash of UA + random device id).  
- **Logout everywhere**: Server‑side invalidation list.

**Recovery & Verification**  
- Email verification mandatory (secure magic link, 15‑minute expiry).  
- Secure password reset with rate limiting + IP reputation; never reveal whether email exists in error text.

**Error Handling**  
- Do not leak existence of accounts: generic messages ("If an account exists, you’ll receive an email").  
- Centralized error codes; user-friendly messages; no stack traces to client.  
- Telemetry for auth errors (anonymized) to detect brute force patterns.

---

## 5) Authorization
- Enforce ownership checks for read/update/delete of contributions.  
- Moderation and admin actions gated by RBAC; all privileged operations audited.  
- Server-side checks only; never trust client flags.

---

## 6) Transport & Storage Security
- **TLS 1.2+** for all endpoints; HSTS (max‑age ≥ 6 months).  
- **At rest:**
  - DB encryption at rest (Atlas/Firestore default).  
  - Media storage: enforce provider-side encryption; prefer customer-managed keys if available.  
  - Client offline cache: encrypt queued payloads with AES‑GCM; store only minimal metadata; provide "Clear offline data" control.

---

## 7) Upload & Media Security
- **Validation:** Strict MIME/type sniffing; whitelists per media type; size/duration caps (e.g., text ≤ 200KB, image ≤ 10MB, audio ≤ 25MB, video ≤ 100MB in MVP).  
- **Transcoding/Sanitization:**
  - Images: strip EXIF/GPS by default; create safe derivatives.  
  - Audio/Video: transcode to safe codecs/containers; normalize loudness; remove embedded subtitles/metadata unless needed.  
  - Text: sanitize HTML/markdown; block scripts.  
- **Malware scanning:** Run **ClamAV** or provider AV on server side for all binaries.  
- **NSFW/illegal content filter:** First-pass via open-source classifiers; human review queue for edge cases.  
- **Deduplication:** Perceptual hashing (pHash/aHash) & SHA‑256 to reduce spam and storage.  
- **Rate limiting & quotas:** Per user/IP/category; burst + sustained limits.  
- **Content provenance:** Record hash, upload time, uploader, consent/license; optional source URL.

---

## 8) Offline‑First & Sync Security
- **Local queue encryption** with per-user key derived from passphrase or token-bound secret.  
- **Conflict handling:** Last‑writer‑wins with audit trail; expose "replace/merge" UI.  
- **Replay protection:** Include server nonce/timestamps; reject duplicates by content hash + nonce window.  
- **Graceful failures:** Retriable errors; exponential backoff; user‑visible sync status.

---

## 9) Privacy, Consent & Licensing
- **Consent UI:** Explicit consent for public display and for research reuse; default to internal until consent given.  
- **License options:** CC‑BY, CC‑BY‑SA, CC0; record per item; display badge.  
- **Sensitive content:** Disallow uploads containing private health/financial data; warn against PII in media/text.  
- **Data Subject Rights:** View/export/delete own contributions; delete account (with content removal or license‑preserving anonymization).  
- **Regional compliance:**
  - Align with **India DPDP Act 2023** basics (notice, consent, data minimization, security safeguards, breach reporting).  
  - If collecting from EU users, follow GDPR lawful basis (consent), DSR processes.  
- **Children:** Avoid targeted collection from <18; no profiling; age‑gate messaging.

---

## 10) Logging, Monitoring & Audit
- **Application logs:** Auth events, upload actions, moderation decisions; redact PII; structured JSON.  
- **Security logs:** Admin activity, role changes, key operations, token anomalies.  
- **Retention:** 90 days for app logs, 1 year for security/audit logs (configurable).  
- **Alerting:** Thresholds for brute force, unusual upload spikes, AV detections.  
- **Time sync:** All logs in UTC with request id/correlation id.

---

## 11) Third‑Party Services & Config Hardening
- **Firestore Rules / MongoDB Atlas:**
  - Firestore: rules to scope reads/writes to owner; server timestamps; validate fields/types.  
  - Mongo: network peering + IP allowlists; SCRAM auth; disable public access; TLS required.  
- **Storage providers:**
  - Firebase Storage: security rules by uid/path, signed URLs short TTL.  
  - Cloudinary: signed upload presets; invalidate public IDs on delete; strict transformations.  
  - **Avoid IPFS** for non‑public or revocable data (immutable & replicated). If used, pin only items with explicit public consent/license.  
- **Secrets mgmt:** .env not committed; use HF Secrets / GitHub Actions secrets; rotate quarterly and on incident.  
- **CORS:** Restrict origins to production/staging domains; block wildcard in prod.

---

## 12) Availability & Abuse Prevention
- **DoS resilience:** Request timeouts, bandwidth caps for uploads, queued processing, circuit breakers on AV/transcode workers.  
- **Backups:** Daily DB backups with 14–30 day retention; tested restores.  
- **Rate limits:** Auth endpoints stricter; upload endpoints tiered by account age/reputation.  
- **CAPTCHA:** Progressive challenge (hCaptcha) after anomalies.

---

## 13) Secure SDLC & Supply Chain
- **Dependency policy:** Pin versions; weekly vulnerability scans (pip‑audit, Safety, npm audit if used); remove unused packages.  
- **SBOM:** Generate (CycloneDX) and publish in repo.  
- **Code reviews:** At least one security-focused review for auth/upload/crypto changes.  
- **Static analysis:** Bandit (Python), semgrep rules for auth, crypto, SSRF, path traversal.  
- **Secrets scanning:** Gitleaks in CI.  
- **CI/CD:** Immutable builds; checksum verification; least-privilege deploy tokens.

---

## 14) Incident Response
- **Playbooks:** Account compromise, malware content, data breach, abusive campaign.  
- **Breach handling:** Triage → contain → assess impact → notify (within regulatory timelines) → postmortem.  
- **User comms:** Clear banner & email templates; recommend password reset/passkey setup.

---

## 15) User-Facing Security UX
- **Dashboard security:** Only show a user’s own stats; rate-limit stats queries; avoid leaking global counts unless intended.  
- **Privacy toggles:** Per‑item visibility and license; bulk update.  
- **Delete/Export:** One-click export (ZIP + JSON manifest); irreversible delete with 7‑day grace.

---

## 16) Non‑Functional Security Requirements (NFRs)
- **Authentication latency:** < 400ms p95 (excluding email delivery).  
- **Upload scan time:** AV decision within 10s p95 (asynchronous publish).  
- **Availability:** 99% monthly for API/UI in MVP.  
- **Crypto:** All randoms from CSPRNG; AES‑GCM for client cache; key sizes 256‑bit; JWT ES256.

---

## 17) Test Plan & Acceptance Criteria
- **Unit/Integration:** Auth (success/fail/lockout), token rotation, RBAC checks, CSRF (if cookie), upload validators.  
- **Security tests:**
  - Brute-force simulation → throttling works.  
  - Token theft attempt → device binding/rotation invalidates.  
  - Malicious file upload (EICAR) → AV blocks + alerts.  
  - EXIF GPS present → stripped in derivatives.  
  - Offline cache theft → encrypted blobs unreadable.  
- **Pen-test checklist:** OWASP ASVS L1/L2 subset; OWASP Top10; file upload cheat sheet; auth cheat sheet.

---

## 18) Implementation Notes (MVP‑Ready)
- **Auth stack:** FastAPI + Authlib (OAuth2 PKCE), Passlib (Argon2id), pyotp (TOTP), webauthn helpers.  
- **Tokens:** PyJWT (ES256); keypair in HF Secrets; rotate via kid headers.  
- **Uploads:** Signed URLs; server pre‑signs after ownership check; process via worker (Celery/RQ).  
- **AV:** ClamAV daemon container; quarantine bucket.  
- **Image:** Pillow/Thumbor; **strip EXIF**; generate web‑optimized derivatives.  
- **Audio/Video:** FFmpeg sandboxed; set max duration/resolution; compute perceptual hashes.  
- **Client offline cache:** IndexedDB; wrap with WebCrypto SubtleCrypto; clear via Settings.

---

## 19) Documentation & Policies
- Public **Security.md** with disclosure policy and contact.  
- **Privacy Policy** (consent, retention, rights).  
- **Acceptable Use Policy** (no hate/illegal content; takedown).  
- **Moderation guidelines** for reviewers.

---

## 20) Open Questions / Future Work
- Full PWA installability & background sync standardization.  
- Reputation system and community moderation tools.  
- Per‑region data residency (if required by partners).  
- Optional KMS-managed keys and customer-supplied encryption keys.

