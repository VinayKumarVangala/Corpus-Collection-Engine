# Product Requirement Document (PRD)

## 1. Project Title  
**Corpus Collection Engine – Preserving Indian Culture & Diversity**  

---

## 2. Problem Statement  
India’s vast cultural and linguistic diversity is not adequately represented in current digital datasets. AI models lack exposure to local idioms, folklore, oral traditions, cultural practices, and visual heritage. Without an initiative to systematically collect authentic contributions across multiple domains, we risk losing invaluable knowledge and failing to build inclusive AI for India.  

---

## 3. Objective  
To design and deploy an **AI-powered, open-source Streamlit application** that enables users to contribute culturally rich data across multiple categories in **all media formats (Text, Image, Audio, Video)**. The app not only collects but also encourages contributions through a **dashboard that showcases individual contributions**.  

---

## 4. MVP Scope (One-Week Build)  

### 4.1 Core Idea: **“Multi-Category Corpus Collector”**  
- **User Benefit**: A simple, engaging platform to upload and preserve local knowledge (stories, proverbs, recipes, traditions, music, photos, videos, etc.) across categories.  
- **Corpus Contribution**: Each contribution—whether text, image, audio, or video—enriches datasets representing India’s diversity.  
- **MVP Deliverables**:  
  - Streamlit app deployed on Hugging Face Spaces.  
  - Categories interface with options like: Art, Meme, Culture, Food, Fables, Events, Music, People, Literature, Architecture, Skills, Images, Videos, Flora, Fauna, Education, Vegetation, Folk Talks, Traditional Skills, Local History, Local Locations, Local Histories, Food & Agriculture, Newspapers.  
  - Upload functionality for text, image, audio, and video.  
  - Basic user dashboard showing contribution stats:  
    - **File Count per media type** (Text, Image, Audio, Video).  
    - **Total Size contributed** (MB/GB).  

---

## 5. Features  

### 5.1 Must-Have (MVP – Week 1)  
- Multi-category submission system.  
- Upload for text, image, audio, video.  
- Metadata tagging (username, category, language).  
- Offline-first caching for uploads.  
- User dashboard showing:  
  - Total contributions.  
  - Number of files per media type.  
  - Contribution size per media type.  

### 5.2 Nice-to-Have (Post-MVP)  
- Gamification: badges/leaderboard for contributors.  
- Advanced analytics (most active categories, trending uploads).  
- AI-based auto-tagging of content (e.g., language detection, media classification).  
- Community gallery with browsing & upvoting.  

---

## 6. Target Users  
- Students, researchers, and history enthusiasts.  
- Communities preserving folk traditions and local knowledge.  
- Youth and meme creators for modern cultural expressions.  
- NGOs, cultural organizations, and local archives.  

---

## 7. AI Integration  
- Open-source AI models (Hugging Face):  
  - **Language Detection** – auto-tag submissions.  
  - **Speech-to-Text** – transcribe audio/video.  
  - **Image/Video Tagging** – metadata enrichment.  
- Optional AI-based recommendations for relevant categories.  

---

## 8. Technical Architecture  

### 8.1 Frontend  
- **Streamlit** for clean, multilingual UI.  
- Category-based navigation grid.  
- Dashboard with charts (file count & size per type).  

### 8.2 Backend  
- **FastAPI/Flask** for APIs (optional, if scaling).  
- Database: **Firebase Firestore (free tier)** or **MongoDB Atlas**.  
- Media storage: **Firebase Storage / IPFS / Cloudinary (free tier)**.  

### 8.3 Hosting & Deployment  
- Hugging Face Spaces (primary deployment).  
- Git-based CI/CD.  

### 8.4 Data Storage  
- Structured storage:  
  - Metadata (JSON): userID, username, category, language, timestamp, media type.  
  - Media: stored in storage bucket with references in DB.  

---

## 9. Offline-First Design  
- Local caching of media & metadata.  
- Background sync when connected.  
- Lightweight metadata requests to minimize bandwidth.  

---

## 10. Success Metrics  

- **User Acquisition**: Number of unique contributors in 2 weeks.  
- **Corpus Collected**:  
  - Number of submissions across categories.  
  - Total dataset size.  
- **Diversity**: Languages, regions, and categories represented.  
- **Engagement**: Avg. number of contributions per user.  

---

## 11. Project Lifecycle & Roadmap  

### Week 1: **Development Sprint**  
- Build & deploy MVP with category selection + multi-format upload.  
- Implement dashboard showing user contributions (size + count).  

### Week 2: **Testing & Iteration**  
- Recruit 20–30 testers from student groups & local communities.  
- Collect feedback on usability, media upload stability, offline mode.  
- Iterate: bug fixes + UI polish.  

### Weeks 3–4: **User Acquisition & Growth**  
- Launch outreach campaign:  
  - WhatsApp/Telegram community drives.  
  - Collaborations with cultural/literary groups.  
  - Meme & story-sharing contests to attract youth.  
- Track contributions across categories.  

### Post-Internship Vision  
- Expand dashboard with analytics & gamification.  
- Build browsing community gallery.  
- Create category-specific leaderboards.  
- Scale corpus export for researchers & AI developers.  

---

## 12. Risks & Mitigations  

- **High storage costs** → Use free-tier + compress media.  
- **Low user adoption** → Category diversity ensures broader appeal.  
- **Spam/irrelevant uploads** → Add moderation workflows.  
- **Bandwidth issues** → Offline-first design + lightweight metadata sync.  

---

## 13. Deliverables  

- Public repo on **code.swecha.org** with:  
  - `README.md`  
  - `REPORT.md`  
  - `CONTRIBUTING.md`  
  - `CHANGELOG.md`  
  - `requirements.txt`  
  - `LICENSE`  
  - Clean, well-documented code  

- Live deployed app on Hugging Face Spaces with public access.  

