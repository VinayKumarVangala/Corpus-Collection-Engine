# Frontend Guideline — Corpus Collection Engine

**Purpose:** A practical, developer-friendly frontend guideline to build a smooth, engaging, and accessible Streamlit UI for the Multi-Category Corpus Collector. This guide focuses on UX patterns, responsive UI, offline-first behavior, media upload flows, dashboards, performance, accessibility, localization, error handling, and dev best practices to ship a production-feeling app within the 1-week MVP timeline.

---

## 1. Design Principles
- **Utility-first & Delightful:** Prioritize quick task completion (uploading, browsing, sharing) while adding micro-interactions that delight (animations, progress states, friendly copy).  
- **Minimal cognitive load:** One clear primary action per screen. Keep forms short and progressive.  
- **Mobile-first & responsive:** Assume most contributors will use phones. Optimize for portrait layout and small screens.  
- **Offline-friendly:** Make the app usable when offline — queue uploads and show clear sync state.  
- **Inclusive & local:** Provide multilingual UI, accessible controls, and clear affordances for low-literacy users.

---

## 2. Layout & Navigation
- **Top area (global header):** App logo + name, language switcher (prominent), user avatar/menu (login/upload stats), primary action button ("Contribute").  
- **Left/Top navigation:** For desktop, a compact left rail with category grid + search filter. For mobile, a bottom nav bar with: Home, Contribute, Browse, Dashboard, Profile.  
- **Category Grid (homepage):** Large tappable cards for each category (Art, Meme, Culture, Food, Fables, Events, Music, People, Literature, Architecture, Skills, Images, Videos, Flora, Fauna, Education, Vegetation, Folk Talks, Traditional Skills, Local History, Local Locations, Local Histories, Food & Agriculture, Newspapers). Each card shows icon, short description, and count badge (if available).  
- **Contextual help:** Small info (?) icons on complex views; include a quick walkthrough (first-time carousel) for contributors.

---

## 3. Contribution Flow (Primary UX)
Goal: Make contributing text/image/audio/video frictionless and safe.

### 3.1 Entry points
- Prominent "Contribute" CTA in header and on category cards.
- In-feed quick upload chips (e.g., "Add photo", "Record audio") for mobile.

### 3.2 Progressive Form Pattern
- Step 1: Choose Category (or detect via context).  
- Step 2: Choose Media Type (Text / Image / Audio / Video).  
- Step 3: Provide Content — keep single-field focus: text editor, image picker + crop, audio recorder, video recorder or file picker.  
- Step 4: Metadata — language (detect & editable), title/short description (optional), location (coarse; opt-in), licensing & consent toggle.  
- Step 5: Review & Submit — show size estimate, preview, and privacy setting (public/internal).  

### 3.3 Mobile-specific UX
- Use native file pickers; integrate camera and microphone permissions gracefully.  
- Provide inline recording controls with clear visual meters and max-duration counter.  
- Offer low-resolution upload option (compressed) with explanation of savings.

### 3.4 Offline queuing & Sync
- When offline, let user "Save offline" — store encrypted bundle in IndexedDB with metadata.  
- Show a local queue panel in profile/dashboard with per-item status (pending, failed, synced).  
- Auto-sync on connectivity; provide manual "Sync now" and robust retry logic.

---

## 4. Media Upload UX
- **Client-side validation:** Show immediate file size/type warnings before upload.  
- **Progress & feedback:** Chunked uploads with progress bar, ETA, and cancel button. Visual placeholder while server processes (scanning/transcoding).  
- **Preview:** For images/videos show a thumbnail; for audio show waveform or simple play button with duration; for text show snippet.  
- **Compression modes:** Offer "Original" and "Optimized (recommended)" choices; default to optimized for low bandwidth.  
- **Sanitization messages:** If EXIF removed or text sanitized, show a short note so users understand transformations.

---

## 5. Dashboard & Analytics UX
- **Per-user dashboard:** Visible after login; key sections: Contribution Summary, Media Breakdown, Recent Uploads, Sync Queue, Badges/Progress (if enabled).  
- **Contribution Summary widgets (top row):**  
  - Total data size contributed (humanized: MB/GB).  
  - Total files contributed.  
  - Files by type (Text/Image/Audio/Video) — count + size.  
  - Active categories count.  
- **Charts:** Use simple, readable charts (bar for counts by media, donut for size distribution). Keep one chart per row.  
- **Recent Uploads list:** Thumbnail, title, category, media type, size, visibility, timestamp. Actions: edit metadata, delete, change visibility.  
- **Export:** One-click export (ZIP + manifest JSON) for user's data.  

---

## 6. Browse & Search
- **Global search:** Search by keyword, language, category, and tag. Support fuzzy matches.  
- **Filters:** Language, date, media type, category.  
- **Infinite scroll vs pagination:** Use infinite scroll with sentinel loading for feed; preserve scroll position.  
- **Card design:** Clean cards with thumbnail, brief caption, language tag, category badge, and a small share button.

---

## 7. Authentication & Profile UX
- **Lightweight signup:** Email + display name or social sign-in; encourage passkeys/WebAuthn when available.  
- **Onboarding:** After signup, guide user to make first contribution via quick action.  
- **Profile:** Editable display name, languages spoken, public handle, contribution stats, privacy settings.  
- **Friendly error handling:** Non-technical messages; avoid account-existence leaks. Provide inline help links for auth issues.

---

## 8. Accessibility & Internationalization
- **WCAG basics:** Semantic HTML where possible, keyboard navigation, focus outlines, ARIA labels for dynamic components.  
- **Contrast & font:** Use high-contrast color tokens; scalable fonts and generous line spacing.  
- **Localization:** Externalize all strings; support LTR + future RTL. Default languages: English + top regional languages (Hindi, Telugu, Tamil, Kannada, Bengali, Marathi, Gujarati, Malayalam, Punjabi, Odia, Assamese).  
- **Simplified mode:** Alternate UI with larger text and simpler controls for low-literacy users.

---

## 9. Performance & Offline Considerations
- **Lazy load assets:** Load category images, templates, and heavy components on demand.  
- **Optimized images:** WebP/JPEG 80% for thumbnails, serve responsive sizes.  
- **Chunked uploads:** Break large media into chunks with resumable upload.  
- **Minimize round trips:** Batch metadata updates; use optimistic UI for snappy responses.  
- **Service worker / PWA (optional):** Cache static assets and provide offline shell.

---

## 10. Error Handling & Notifications
- **Global toast system:** Non-blocking toasts for success, warning, errors with retry actions.  
- **Inline validation:** Immediate form validation with clear hints.  
- **Sync errors:** Per-item retry/fix options; show reason for failures (network, size, malware).  
- **Server errors:** Generic friendly message and a link to support; log details client-side for telemetry.

---

## 11. Micro-interactions & Polishing
- Use subtle motion for transitions (fade/slide) and microcopy that reinforces progress ("Compressing…", "Queued for upload", "Thanks — your contribution helps preserve local heritage!").  
- Provide small confirmations after actions ("Saved to queue", "Upload complete").  
- Use skeleton loaders for lists and previews to avoid content jumps.

---

## 12. Security & Privacy UX
- **Consent flows:** Explicit checkboxes for public sharing and license selection; default to "Internal" unless user opts-in.  
- **Privacy reminders:** Inline notices when location data or PII detected; offer to redact before submit.  
- **2FA prompts:** Contextual nudges to enable passkeys or TOTP with clear benefits.

---

## 13. Component Library & Streamlit Patterns
- **UI primitives:** Use Streamlit + st.components for custom widgets (multi-step modal, recorder, waveform, image cropper). Consider third-party components:  
  - `streamlit-drag-and-drop` for uploads.  
  - `streamlit-webrtc` for audio/video capture (live recording).  
  - `streamlit-aggrid` for tabular lists.  
  - `streamlit-chat` or simple custom chat-like UI for guided flows.  
- **Custom components:** Build small React components for recorders, cropping, progress with `st.components.v1` and ship minimal, well-documented bindings.  
- **Theming:** Define a consistent token set (primary, secondary, bg, surface, success, warning, error) and reuse.

---

## 14. Developer Notes & Folder Structure
- `frontend/streamlit_app.py` — main app entry.  
- `frontend/components/` — custom components (React) + wrappers.  
- `frontend/static/` — icons, templates, thumbnails.  
- `frontend/i18n/` — translation json files per language.  
- `frontend/styles/` — CSS/JS for components.  
- `frontend/utils/` — upload helpers, offline queue, compression utilities.  
- Keep UI code modular; each page is a function: `home()`, `contribute()`, `browse()`, `dashboard()`, `profile()`.

---

## 15. Testing & QA
- **Unit test components** where possible; add integration tests for contribution flow (mock uploads).  
- **Manual test matrix:** upload types, languages, offline behavior, low-bandwidth testing (throttled network), mobile OSes, permission flows for camera/mic.  
- **Accessibility audit:** Lighthouse + axe-core checks; fix critical contrast and navigation issues.

---

## 16. Analytics & Instrumentation
- Track critical events (signup, contribution_submit, contribution_sync, contribution_export, login_fail).  
- Respect privacy: anonymize PII; provide opt-out for telemetry.  
- Use lightweight analytics (self-hosted or privacy-first) to measure funnel & drop-offs: how many started contribution vs completed.

---

## 17. Roadmap & UX Enhancements
- Gamification: badges, streaks, leaderboards (post-MVP).  
- Community gallery with curated collections.  
- AI-assisted enhancements: caption suggestions, auto-language tags, recommended categories.  
- Offline-first PWA with background sync and background recording upload.

---

## Appendix: Quick Component Specs
- **Category Card:** 120–160px tile, icon (64px), title, 1-line description, count badge.  
- **Contribution Modal:** Max 3 steps on mobile; Next/Back with progress indicator.  
- **Upload Progress:** Linear progress bar with chunk indicator; cancel & pause.  
- **Audio Recorder:** Record/Stop, Play, Re-record, Trim slider (optional), duration counter.  
- **Video Recorder:** Start/Stop, thumbnail capture, small resolution selector (360p/480p/720p).  

---

This guideline should be used as a living reference while implementing the Streamlit frontend. If you want, I can now:  
- Produce wireframe mockups for the main screens (Home, Contribute, Dashboard, Browse).  
- Generate skeleton Streamlit code (pages + placeholders) implementing the navigation & basic components.  
- Create a checklist for the 7-day frontend sprint with daily milestones.

