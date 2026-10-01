n# CareerMatch AI — AI-Powered Job Recommendation System

> **Find the jobs that fit your skills.**

A production-grade, full-stack AI Job Recommendation System built as a portfolio project for B.Sc. Artificial Intelligence & Data Science graduates. Features an explainable hybrid recommendation engine combining **TF-IDF Cosine Similarity** with **Multi-Factor Weighted Scoring**, interactive skill-gap analysis, a visual Kanban application tracker, and a modern glassmorphism-inspired UI with dark/light mode.

---

## 🎯 Problem Statement

Job seekers in technology face an overwhelming number of job listings across dozens of platforms. Manually comparing skills, education, experience and interests against each posting is tedious and error-prone. CareerMatch AI solves this by:

1. Building a structured digital profile of the candidate (skills, education, experience, interests, location, work mode)
2. Using a transparent, explainable AI recommendation engine to rank and score every job listing
3. Showing **exactly why** each job was recommended and which skills the candidate should learn
4. Providing a complete application lifecycle tracker (Kanban board)

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **AI Job Matching** | Hybrid TF-IDF + Multi-Factor Weighted Scoring ranks 100+ jobs by match percentage |
| **Explainable AI** | Each recommendation shows matched skills, skill gaps, education/experience/location breakdown |
| **Skill Gap Analysis** | Visual comparison of your skills vs. job requirements with learning suggestions |
| **Interactive Skill Chips** | Searchable, clickable skill palette instead of boring text inputs |
| **Kanban Tracker** | Drag-status application tracker (Saved → Applied → Interview → Selected / Rejected) |
| **Analytics Dashboard** | 4 Chart.js visualizations: skill distribution, category fit, app status, score distribution |
| **1-Click Demo Mode** | Instantly login as a pre-configured student (Alex Chen) for placement interviews |
| **Admin Dashboard** | Manage jobs, view users, see system-wide analytics |
| **Dark / Light Mode** | Beautiful glassmorphism-inspired theme toggle |
| **100% Offline** | No external APIs needed — runs entirely on local Python + SQLite |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript, Font Awesome 6, Chart.js 4 |
| **Backend** | Python 3.10+, Flask 3.x |
| **Database** | SQLite 3 with Foreign Keys |
| **AI/ML** | Scikit-learn (TF-IDF Vectorizer, Cosine Similarity), Pandas, NumPy |
| **Security** | Werkzeug password hashing, parameterized SQL, input validation |

---

## 🏗 Architecture

```
career-match-ai/
├── app.py                    # Flask application entry point
├── config.py                 # Configuration & recommendation weights
├── requirements.txt
├── README.md
├── database/
│   ├── database.py           # SQLite connection utilities
│   ├── schema.sql            # Relational schema (8 tables)
│   └── seed_data.py          # 105+ realistic job records, 80+ skills, demo accounts
├── models/
│   ├── user.py               # User auth, profile, skills CRUD
│   └── job.py                # Job search, save, applications, stats
├── ml/
│   ├── preprocessing.py      # Text normalization, skill aliases, corpus builders
│   └── recommendation_engine.py  # TF-IDF + Multi-Factor Scoring + Skill Gap
├── routes/
│   ├── auth.py               # Login, Register, Logout, 1-Click Demo
│   ├── jobs.py               # Search, Detail, Save/Unsave
│   ├── recommendations.py    # AI recommendations, Skill Gap Analysis
│   ├── dashboard.py          # Dashboard, Profile, Applications tracker
│   └── admin.py              # Admin dashboard, Job CRUD, User management
├── templates/                # 15+ Jinja2 templates
│   ├── base.html, index.html
│   ├── auth/ login.html, register.html
│   ├── dashboard/ dashboard.html, profile.html
│   ├── jobs/ recommendations.html, search.html, job_detail.html,
│   │         saved_jobs.html, applications.html, skill_gap.html
│   ├── admin/ dashboard.html, manage_jobs.html, users.html
│   └── errors/ 404.html, 500.html
└── static/
    ├── css/style.css          # Complete design system (1000+ lines)
    └── js/app.js              # Theme, mobile menu, toasts, animations
```

---

## 🗄 Database Design

```
users (id, email, password_hash, full_name, role, created_at)
  │
  ├── profiles (user_id FK → users.id)
  │     education, degree, specialization, graduation_year,
  │     experience_level, preferred_location, work_mode, career_interests
  │
  ├── user_skills (user_id FK, skill_id FK → skills.id)
  │
  ├── saved_jobs (user_id FK, job_id FK → jobs.id)
  │
  └── applications (user_id FK, job_id FK → jobs.id, status, notes)

skills (id, name, category)

jobs (id, title, company, location, work_mode, experience_level,
      salary_min, salary_max, description, job_category, ...)
  │
  └── job_skills (job_id FK, skill_id FK, is_required)
```

---

## 🧠 How the AI Recommendation Engine Works

### Algorithm Overview

The recommendation engine uses a **Hybrid Scoring Approach** combining two ML techniques:

#### 1. TF-IDF Cosine Similarity (Semantic Matching)

- Builds a text "corpus" for each user profile (skills repeated 3x for emphasis + degree + interests + bio)
- Builds a text corpus for each job (required skills 3x + title 2x + description + responsibilities)
- Uses `TfidfVectorizer` with bigrams to convert both into numerical vectors
- Calculates `cosine_similarity` between the user vector and all job vectors
- This captures semantic/contextual similarity beyond exact keyword matching

#### 2. Multi-Factor Weighted Scoring (Explainable Matching)

Five factors are scored independently (0.0 to 1.0) and combined with configurable weights:

| Factor | Weight | How It's Calculated |
|--------|--------|-------------------|
| **Skill Match** | 50% | Weighted Jaccard: required skills worth 1.0, preferred worth 0.4 |
| **Education Match** | 15% | Field relevance (AI/CS/DS keywords) + degree level |
| **Experience Match** | 15% | Perfect if within range, penalized linearly for gaps |
| **Interest Match** | 10% | User career interests mapped to job categories |
| **Location/Mode** | 10% | Work mode compatibility (60%) + city match (40%) |

#### 3. Final Score Blending

```
final_score = (weighted_composite × 0.80) + (tfidf_cosine × 0.20)
match_percentage = min(final_score × 100, 99%)
```

This approach is:
- **Transparent**: Every factor can be shown to the user ("✓ 8 skills matched, ✓ Education aligned")
- **Configurable**: Weights can be tuned in `config.py` without changing code
- **Explainable**: Perfect for placement interview demonstrations

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Step-by-step

```bash
# 1. Navigate to project folder
cd career-match-ai

# 2. (Optional) Create virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install flask scikit-learn pandas numpy

# 4. Run the application
python app.py
```

The database is automatically created and seeded with 105+ jobs on first run.

### Access the Application

| URL | Purpose |
|-----|---------|
| http://127.0.0.1:5000/ | Landing page |
| http://127.0.0.1:5000/demo-login | 1-Click Student Demo Login |
| http://127.0.0.1:5000/admin-demo-login | 1-Click Admin Demo Login |

### Demo Credentials

| Account | Email | Password |
|---------|-------|----------|
| **Student (Alex Chen)** | demo@careermatch.ai | demo123 |
| **Admin** | admin@careermatch.ai | admin123 |

---

## 🎤 Placement Interview Demo Flow

1. Open `http://127.0.0.1:5000/` → Show the landing page
2. Click **"1-Click Demo"** → Instantly logged in as Alex Chen
3. Navigate to **Dashboard** → Show profile completion, stats, charts
4. Go to **Profile** → Demonstrate interactive skill chip selector
5. Click **"AI Jobs"** → Show ranked recommendations with match scores
6. Click a **job card** → Show "Why this job matches you" + skill gap breakdown
7. Click **"Skill Gap Analysis"** → Show visual comparison + learning suggestions
8. **Save** and **Apply** to a job → Show toast notifications
9. Go to **Application Tracker** → Show Kanban board with status columns
10. Toggle **Dark Mode** → Show responsive, polished UI
11. Login as **Admin** → Show admin dashboard with system analytics

---

## 💡 Interview Questions & Answers

**Q1: What algorithm does your recommendation engine use?**
> It uses a hybrid approach: TF-IDF Cosine Similarity for semantic text matching, combined with a Multi-Factor Weighted Scoring system that evaluates skill match (50%), education (15%), experience (15%), career interests (10%), and location/work mode (10%).

**Q2: Why TF-IDF instead of deep learning?**
> TF-IDF is lightweight, interpretable, and doesn't require GPU or large training data. For a job matching system with structured skill data, the weighted scoring provides better explainability than a black-box neural network. In production, this could be extended with word embeddings.

**Q3: How do you handle the cold-start problem?**
> New users are prompted to complete their profile and select skills immediately. The skill chip interface makes this fast and intuitive. Even with minimal data (just skills), the engine can produce meaningful matches.

**Q4: How is the match score calculated?**
> Each of 5 factors (skills, education, experience, interests, location) is scored 0-1, then multiplied by configurable weights. The weighted sum is blended 80/20 with TF-IDF cosine similarity. The final score is displayed as a percentage.

**Q5: What database did you use and why?**
> SQLite — it's serverless, zero-configuration, and perfect for a portfolio project. The schema uses proper foreign keys, indexes, and parameterized queries for security. In production, this could be swapped for PostgreSQL.

**Q6: How do you prevent SQL injection?**
> All database queries use parameterized placeholders (?) instead of string concatenation. User inputs are validated on the server side before processing.

**Q7: How does the skill gap analysis work?**
> It compares the user's skill set against the job's required and preferred skills using set intersection/difference operations, then presents matched skills (✓) and missing skills (△) with learning suggestions.

---

## 📝 Resume Description

> **CareerMatch AI — AI-Powered Job Recommendation System**
> Built a full-stack AI job recommendation platform using Flask, SQLite, and Scikit-learn. Implemented a hybrid recommendation engine combining TF-IDF Cosine Similarity with Multi-Factor Weighted Scoring across 5 dimensions (skills, education, experience, interests, location). Features include interactive skill selection, explainable match breakdowns, visual skill-gap analysis, Kanban application tracker, Chart.js analytics dashboard, and admin panel. Seeded with 105+ realistic tech job listings and 80+ categorized skills.

---

## 🔮 Future Improvements

- Collaborative filtering (recommend based on similar users' preferences)
- Resume PDF upload and automatic skill extraction using NLP
- Real-time job API integration (LinkedIn, Indeed)
- Email notifications for new matches
- Deployed version on Heroku/Railway/Render
- User-to-user networking features
- Mobile app with React Native

---

## 📜 License

This project is created for educational and portfolio purposes. Sample data is fictional.

---

*Built with ❤️ for AI & Data Science students preparing for placement interviews.*
