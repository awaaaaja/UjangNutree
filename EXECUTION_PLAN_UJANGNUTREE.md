# Execution Plan: UjangNutree

> Rebuild Nutribase → **UjangNutree**  
> Mobile-First | Tablet-Ready | AI-Powered  
> GitHub: https://github.com/awaaaaja/UjangNutree

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Roadmap & Timeline](#2-roadmap--timeline)
3. [Phase 0: Foundation](#3-phase-0-foundation)
4. [Phase 1: Scraping & Dataset](#4-phase-1-scraping--dataset)
5. [Phase 2: Backend API](#5-phase-2-backend-api)
6. [Phase 3: Frontend Mobile-First](#6-phase-3-frontend-mobile-first)
7. [Phase 4: ML Service](#7-phase-4-ml-service)
8. [Phase 5: Integration & Testing](#8-phase-5-integration--testing)
9. [Phase 6: Deployment & Docs](#9-phase-6-deployment--docs)
10. [Git Workflow](#10-git-workflow)
11. [Commit Convention](#11-commit-convention)
12. [Directories Structure](#12-directories-structure)

---

## 1. Project Overview

### What is UjangNutree?
A **mobile-first nutrition database & meal planning platform** rebuilt from Nutribase, targeting:
- **Ahli Gizi / Dietisien** — manage patients, calculate intake, AKG analysis
- **Mahasiswa Gizi** — learn & practice with real food data
- **UMKM Food** — access nutritional data for product labeling

### Key Improvements over Nutribase:
| Aspek | Nutribase (Existing) | UjangNutree (Rebuild) |
|-------|---------------------|-----------------------|
| **UI/UX** | Element Plus (desktop-first) | Tailwind + shadcn/vue (mobile-first) |
| **Responsive** | Desktop only | Mobile S → Tablet → Desktop |
| **Search** | Basic LIKE query | Meilisearch full-text |
| **ML** | None | Hybrid recommendation engine |
| **Performance** | Unoptimized | PWA, lazy loading, caching |
| **Testing** | Minimal | 80%+ coverage |
| **CI/CD** | None | GitHub Actions automated |

### Tech Stack:
```
Frontend:   Nuxt 3 + Tailwind CSS + shadcn-vue + Pinia
Backend:    Laravel 11 + Sanctum + Meilisearch + Reverb
ML:         Python FastAPI + scikit-learn + pgvector
Database:   PostgreSQL + Redis
Infra:      Docker + GitHub Actions + VPS/Cloud
```

---

## 2. Roadmap & Timeline

```
MINGGU 1-2  ████████████░░░░░░░░░░░░░░░░  Foundation + Scraping
MINGGU 3-4  ████████████████░░░░░░░░░░░░  Backend API (MVP)
MINGGU 5-6  ██████████████████████░░░░░░  Frontend (Mobile-First)
MINGGU 7    ██████████████████████████░░  ML Service
MINGGU 8    ████████████████████████████  Testing + Deploy
```

| Phase | Minggu | Output |
|-------|--------|--------|
| **0 — Foundation** | 1 | Repo, Docker, struktur folder, DB schema |
| **1 — Scraping** | 1-2 | 2000+ food entries, normalized dataset |
| **2 — Backend API** | 3-4 | 36+ endpoints, auth, search, docs |
| **3 — Frontend** | 5-6 | 18 pages mobile-first, PWA, i18n |
| **4 — ML Service** | 7 | Hybrid recommendation engine |
| **5 — Integration** | 7-8 | API + Frontend + ML integration |
| **6 — Testing** | 8 | E2E, unit, performance, deploy |

---

## 3. Phase 0: Foundation

### 3.1 Repository & Structure

```bash
# Init repository
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/awaaaaja/UjangNutree.git
git push -u origin main
```

### 3.2 Directory Structure

```
ujangnutree/
├── frontend/                    # Nuxt 3 (Mobile-First)
│   ├── app/                     # Nuxt 3 app directory
│   │   ├── layouts/             # default.vue (mobile+tablet+desktop)
│   │   ├── pages/               # 18 routes
│   │   ├── components/          # Shared components
│   │   ├── composables/         # useApi, useAuth, etc.
│   │   ├── stores/              # Pinia stores
│   │   ├── i18n/                # id.json, en.json
│   │   └── middleware/          # Auth middleware
│   ├── public/                  # Static assets
│   ├── tailwind.config.ts
│   ├── nuxt.config.ts
│   └── package.json
│
├── backend/                     # Laravel 11 API
│   ├── app/
│   │   ├── Http/
│   │   │   ├── Controllers/Api/
│   │   │   ├── Requests/
│   │   │   └── Resources/
│   │   ├── Models/
│   │   ├── Services/
│   │   └── Rules/
│   ├── database/
│   │   ├── migrations/
│   │   └── seeders/
│   ├── routes/
│   │   └── api.php
│   ├── tests/
│   ├── config/
│   ├── Dockerfile
│   └── composer.json
│
├── ml-service/                  # Python FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── api/
│   │   ├── schemas/
│   │   └── rules/
│   ├── training/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── scraping/                    # Data collection
│   ├── scripts/
│   ├── output/
│   │   ├── raw/
│   │   ├── normalized/
│   │   └── final/
│   ├── logs/
│   └── README.md
│
├── database/                    # Schema & migrations
│   ├── schema.sql
│   ├── erd.md
│   └── seed/
│
├── docs/
│   ├── PRD.md
│   ├── API.md
│   ├── ARCHITECTURE.md
│   └── MOBILE_GUIDELINES.md
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   └── deploy.yml
│   └── CODEOWNERS
│
├── docker-compose.yml
├── AGENTS.md
└── README.md
```

### 3.3 Docker Development Setup

```yaml
# docker-compose.yml
services:
  frontend:
    image: node:20
    ports: ["3000:3000"]
    volumes: [./frontend:/app]
    working_dir: /app
    command: npm run dev

  backend:
    image: php:8.3-fpm
    ports: ["8000:8000"]
    volumes: [./backend:/app]
    depends_on: [database, meilisearch, redis]

  database:
    image: postgres:16
    ports: ["5432:5432"]
    environment:
      POSTGRES_DB: ujangnutree
      POSTGRES_PASSWORD: secret

  meilisearch:
    image: getmeili/meilisearch:v1.7
    ports: ["7700:7700"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
```

---

## 4. Phase 1: Scraping & Dataset

### 4.1 Target Sources

| Source | Type | Target Records | Tool |
|--------|------|---------------|------|
| **panganku.org** (TKPI) | Web scraping | 1,500+ foods | Scrapy |
| **USDA FoodData Central** | API | 500+ foods | requests + API key |
| **BPOM RI** | Public data | 300+ products | BeautifulSoup |
| **Manual Entry** | Expert input | 200+ recipes | CSV import |

### 4.2 Execution Steps

```bash
# 1. Setup virtual environment
cd scraping
python -m venv venv
source venv/bin/activate
pip install scrapy requests beautifulsoup4 pandas

# 2. Scrape TKPI
python scripts/scrape_panganku.py
# Output: output/raw/panganku_YYYYMMDD.json
# Commit: git commit -m "scrape(tkpi): add raw data from panganku.org"

# 3. Scrape USDA
python scripts/scrape_usda.py
# Output: output/raw/usda_YYYYMMDD.json
# Commit: git commit -m "scrape(usda): add data from USDA FoodData Central"

# 4. Normalize all data
python scripts/normalize.py
# Output: output/normalized/foods_normalized.json
# Commit: git commit -m "scrape(normalize): merge & normalize all food data"

# 5. Generate final dataset for DB import
python scripts/generate_final.py
# Output: output/final/foods_final.csv + foods_final.json
# Commit: git commit -m "scrape(final): generate production-ready dataset"
```

### 4.3 Food Schema (Final)

```json
{
  "id": "uuid-string",
  "name": "Nasi Putih",
  "name_en": "White Rice",
  "category": "Makanan Pokok",
  "sub_category": "Serealia",
  "brand": null,
  "source": "tkpi",
  "serving_size_g": 100,
  "serving_desc": "1 centong (100g)",
  "energy_kcal": 180,
  "protein_g": 3.0,
  "fat_g": 0.3,
  "carbohydrate_g": 39.8,
  "fiber_g": 0.3,
  "water_g": 56.6,
  "ash_g": 0.3,
  "vitamin_a_mcg": 0,
  "vitamin_c_mg": 0,
  "calcium_mg": 5,
  "phosphorus_mg": 40,
  "iron_mg": 0.4,
  "sodium_mg": 2,
  "potassium_mg": 30,
  "zinc_mg": 0.7,
  "tags": ["rice", "staple", "indonesian"],
  "allergens": [],
  "verification_status": "verified",
  "metadata": {
    "original_id": "TKPI-001",
    "source_url": "https://www.panganku.org/...",
    "scraped_at": "2026-07-09"
  }
}
```

---

## 5. Phase 2: Backend API

### 5.1 Database Migrations (Urutan Eksekusi)

```bash
# Buat migrations sesuai urutan dependency
php artisan make:migration create_users_table
php artisan make:migration create_age_groups_table
php artisan make:migration create_maternal_statuses_table
php artisan make:migration create_food_categories_table
php artisan make:migration create_foods_table
php artisan make:migration create_nutrients_table
php artisan make:migration create_akg_profiles_table
php artisan make:migration create_patients_table
php artisan make:migration create_recipes_table
php artisan make:migration create_recipe_foods_table
php artisan make:migration create_intakes_table
php artisan make:migration create_intake_details_table
php artisan make:migration create_feedbacks_table

# Seed awal
php artisan db:seed --class=AgeGroupSeeder
php artisan db:seed --class=MaternalStatusSeeder
php artisan db:seed --class=FoodCategorySeeder
php artisan db:seed --class=AkgProfileSeeder
php artisan db:seed --class=FoodSeeder  # Import dari hasil scraping

# Commit
git add database/
git commit -m "db(schema): add all migrations & seeders"
```

### 5.2 API Endpoints Checklist

```
AUTH ───────────────────────────────────────────── [ ]
  ✓ POST   /api/auth/login                        [ ]
  ✓ POST   /api/auth/register                     [ ]
  ✓ POST   /api/auth/login/google                 [ ]
  ✓ POST   /api/auth/logout                       [ ]
  ✓ POST   /api/auth/forgot-password              [ ]
  ✓ POST   /api/auth/reset-password               [ ]
  ✓ PUT    /api/auth/user/password                [ ]
  ✓ PUT    /api/auth/user/profile                 [ ]
  ✓ GET    /api/auth/user                         [ ]

DASHBOARD ──────────────────────────────────────── [ ]
  ✓ GET    /api/dashboard/stats                   [ ]

PATIENTS ───────────────────────────────────────── [ ]
  ✓ GET    /api/patients                          [ ]
  ✓ POST   /api/patients                          [ ]
  ✓ GET    /api/patients/{id}                     [ ]
  ✓ PUT    /api/patients/{id}                     [ ]
  ✓ DELETE /api/patients/{id}                     [ ]

INTAKES ────────────────────────────────────────── [ ]
  ✓ GET    /api/patients/{id}/intakes             [ ]
  ✓ POST   /api/patients/{id}/intakes             [ ]
  ✓ GET    /api/intakes/{id}                      [ ]
  ✓ PUT    /api/intakes/{id}                      [ ]
  ✓ DELETE /api/intakes/{id}                      [ ]
  ✓ POST   /api/intakes/{id}/calculate-akg        [ ]
  ✓ PATCH  /api/intakes/{id}/lock                 [ ]
  ✓ PATCH  /api/intakes/{id}/cancel               [ ]

FOODS ──────────────────────────────────────────── [ ]
  ✓ GET    /api/foods                             [ ]
  ✓ GET    /api/foods/{id}                        [ ]
  ✓ POST   /api/foods                             [ ]
  ✓ PUT    /api/foods/{id}                        [ ]
  ✓ DELETE /api/foods/{id}                        [ ]
  ✓ GET    /api/foods/search?q=                   [ ] (Meilisearch)

RECIPES ────────────────────────────────────────── [ ]
  ✓ GET    /api/recipes                           [ ]
  ✓ POST   /api/recipes                           [ ]
  ✓ GET    /api/recipes/{id}                      [ ]
  ✓ PUT    /api/recipes/{id}                      [ ]
  ✓ DELETE /api/recipes/{id}                      [ ]
  ✓ POST   /api/recipes/{id}/foods                [ ]
  ✓ DELETE /api/recipes/{id}/foods/{foodId}       [ ]

AKG ────────────────────────────────────────────── [ ]
  ✓ GET    /api/akg-profiles                      [ ]
  ✓ GET    /api/akg-profiles/{id}                 [ ]

FEEDBACK ───────────────────────────────────────── [ ]
  ✓ GET    /api/feedbacks                         [ ]
  ✓ POST   /api/feedbacks                         [ ]

SETTINGS ───────────────────────────────────────── [ ]
  ✓ GET    /api/settings/contact                  [ ]
  ✓ PUT    /api/settings/contact                  [ ]

SELECT REFERENCE ───────────────────────────────── [ ]
  ✓ GET    /api/select/foods                      [ ]
  ✓ GET    /api/select/patients                   [ ]
  ✓ GET    /api/select/age-groups                 [ ]
  ✓ GET    /api/select/maternal-statuses          [ ]
  ✓ GET    /api/select/recipes                    [ ]
```

### 5.3 Backend Execution

```bash
# 1. Setup Laravel
composer create-project laravel/laravel backend
cd backend
composer require laravel/sanctum
composer require laravel/socialite  # Google OAuth
composer require meilisearch/meilisearch-php
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"

# 2. Buat models & controllers
php artisan make:model Patient -mcr
php artisan make:model Intake -mcr
php artisan make:model IntakeDetail -mcr
php artisan make:model Food -mcr
php artisan make:model Recipe -mcr
php artisan make:model RecipeFood -mcr
php artisan make:model AkgProfile -mcr
php artisan make:model Feedback -mcr

# 3. Testing
php artisan make:test Feature/AuthTest --pest
php artisan make:test Feature/PatientTest --pest
php artisan make:test Feature/IntakeTest --pest
php artisan make:test Feature/FoodTest --pest
php artisan make:test Feature/RecipeTest --pest
php artisan make:test Feature/AkgTest --pest

# 4. Git commits
git add backend/
git commit -m "feat(api): add auth endpoints with sanctum"
git commit -m "feat(api): add patient CRUD endpoints"
git commit -m "feat(api): add intake & AKG calculation endpoints"
git commit -m "feat(api): add food & recipe endpoints with meilisearch"
git commit -m "feat(api): add feedback & settings endpoints"
git commit -m "test(api): add feature tests for all endpoints"
```

---

## 6. Phase 3: Frontend Mobile-First

### 6.1 Design System — Breakpoints

```css
/* Mobile-First Breakpoints */
/* Base: 375px (Mobile S) — NO MEDIA QUERY needed */

/* sm: 640px — Large phone */
/* md: 768px — Tablet portrait */
/* lg: 1024px — Tablet landscape / Small desktop */
/* xl: 1280px — Desktop */
/* 2xl: 1536px — Large desktop */
```

### 6.2 Component Library (Custom, NO Element Plus)

```
components/
├── ui/                          # Base UI components (shadcn-vue style)
│   ├── Button.vue
│   ├── Input.vue
│   ├── Card.vue
│   ├── Dialog.vue               → BottomSheet.vue (mobile)
│   ├── Select.vue
│   ├── Skeleton.vue
│   ├── Progress.vue
│   └── Badge.vue
├── layout/
│   ├── BottomNav.vue            # Mobile bottom navigation
│   ├── Sidebar.vue              # Tablet/Desktop sidebar
│   ├── Header.vue
│   └── MobileNav.vue
├── feature/
│   ├── FoodSearch.vue           # Search bar + infinite scroll
│   ├── NutritionCard.vue        # Nutrient display card
│   ├── IntakeList.vue           # Swipeable intake items
│   ├── AkgProgress.vue          # AKG progress bars
│   ├── PatientCard.vue          # Patient list card
│   └── RecipeCard.vue           # Recipe grid card
└── shared/
    ├── EmptyState.vue
    ├── ErrorState.vue
    ├── NetworkIndicator.vue
    └── PullToRefresh.vue
```

### 6.3 Page Implementation Priority

```
Phase 1 — Auth & Layout (Week 5)
────────────────────────────────
[ ] Layout: BottomNav.vue (mobile) + Sidebar.vue (tablet+)
[ ] /sign-in — Mobile-optimized login
[ ] /sign-up — Full-screen register
[ ] /forgot-password

Phase 2 — Core Features (Week 5-6)
────────────────────────────────
[ ] / — Dashboard (KPI cards vertical stack)
[ ] /patients — Card list + pull-to-refresh
[ ] /patients/:id — Tab layout (Profile | Intakes | Charts)
[ ] Create/Edit patient — Bottom sheet

Phase 3 — Calculator (Week 6)
────────────────────────────────
[ ] /calculator — Sticky search bar, scrollable results
[ ] Intake form — Add food + portion
[ ] AKG visualization — Progress bars
[ ] Lock/Cancel intake

Phase 4 — Database (Week 6)
────────────────────────────────
[ ] /database/foods — Infinite scroll + Meilisearch
[ ] /database/akg-profiles — Filterable list
[ ] /recipes — Grid 2 cols mobile, 3 cols tablet

Phase 5 — Settings (Week 6)
────────────────────────────────
[ ] /settings — Native-style list
[ ] /settings/profile
[ ] /settings/security
[ ] /send-feedback
```

### 6.4 Mobile UX Checklist

```
□ Touch targets semua elemen ≥ 44x44px
□ Bottom sheet untuk form/modal (mobile)
□ Bottom sheet untuk konfirmasi delete
□ Native-like scroll (smooth, momentum)
□ Pull-to-refresh di semua list page
□ Infinite scroll / pagination
□ Skeleton loading setiap page load
□ Empty state dengan illustration
□ Error state dengan retry button
□ Network offline indicator
□ Sticky header untuk search bar
□ Fixed bottom action button (CTA)
□ Swipe-to-delete untuk intake items
□ Safe area insets (notch, home indicator)
```

### 6.5 Frontend Execution

```bash
# 1. Init Nuxt 3
npx nuxi@latest init frontend
cd frontend
npm install
npm install -D tailwindcss @tailwindcss/vite
npm install pinia @pinia/nuxt
npm install @vueuse/core
npm install @nuxtjs/i18n
npm install @nuxtjs/pwa
npm install @nuxt/image
npm install @nuxt/icon
npm install radix-vue  # shadcn-vue dependencies
npm install class-variance-authority
npm install clsx tailwind-merge

# 2. Configure tailwind for mobile-first
# tailwind.config.ts with custom breakpoints

# 3. Build components & pages

# 4. Git commits
git add frontend/
git commit -m "feat(ui): add mobile-first layout with bottom nav"
git commit -m "feat(page): add sign-in & sign-up responsive pages"
git commit -m "feat(page): add patient management mobile pages"
git commit -m "feat(page): add calculator with AKG visualization"
git commit -m "feat(page): add food database with infinite scroll"
git commit -m "feat(page): add recipe pages grid responsive"
```

---

## 7. Phase 4: ML Service

### 7.1 Setup

```bash
# 1. Init FastAPI
cd ml-service
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn scikit-learn pandas numpy
pip install psycopg2-binary pgvector
pip install redis mlflow pytest

# 2. Project structure
mkdir app app/models app/api app/schemas app/rules training tests

# 3. Git commits
git add ml-service/
git commit -m "feat(ml): add hybrid meal recommendation engine"
git commit -m "feat(ml): add rule-based constraints (allergen, diet, disease)"
git commit -m "feat(ml): add cold start strategy & model evaluation"
git commit -m "test(ml): add recommender unit tests"
```

### 7.2 API Endpoint

```
POST /api/v1/recommend/meals

Request:
{
    "patient_id": "uuid",
    "context": {
        "meal_type": "breakfast",
        "target_energy_kcal": 450,
        "target_protein_g": 20,
        "preferences": ["low_carb"],
        "allergies": ["seafood"],
        "max_results": 5
    }
}

Response:
{
    "recommendations": [
        {
            "food": { "id": "uuid", "name": "Omelet Sayur" },
            "nutrition": { "energy": 350, "protein": 18, ... },
            "score": 0.92,
            "reason": "Rendah karbo, protein tinggi, cocok untuk diabetes"
        }
    ],
    "meta": { "model": "hybrid_v2", "inference_ms": 45 }
}
```

---

## 8. Phase 5: Integration & Testing

### 8.1 Integration Checklist

```
Frontend → Backend:
[ ] Auth flow (login/register) complete
[ ] Patient CRUD from frontend
[ ] Calculator flow (search food → add → calculate AKG)
[ ] Recipe management
[ ] Settings & feedback

Backend → ML Service:
[ ] Backend proxy to ML service
[ ] Cache recommendation results in Redis
[ ] Fallback when ML service unavailable

Frontend → ML:
[ ] Recommendation display on dashboard
[ ] "Rekomendasi untuk Anda" widget on calculator page
```

### 8.2 Testing

```bash
# Backend
cd backend
php artisan test --coverage  # Target: 80%

# Frontend
cd frontend
npx vitest run               # Unit test
npx playwright test          # E2E test (mobile viewport)

# ML Service
cd ml-service
pytest --cov=app tests/      # Target: 80%

# CI Pipeline (.github/workflows/ci.yml)
# Auto-run on push & PR
```

---

## 9. Phase 6: Deployment & Docs

### 9.1 Deployment

```bash
# Production build
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Frontend
cd frontend && npm run build
# Deploy to Vercel / Cloudflare Pages / VPS

# Backend
cd backend && php artisan optimize
# Deploy to VPS / Laravel Forge

# ML Service
cd ml-service && docker build -t ujangnutree-ml .
# Deploy to Railway / Render / VPS
```

### 9.2 Documentation

```
docs/
├── PRD.md              # Product Requirements Document
├── ARCHITECTURE.md     # System architecture & ERD
├── API.md              # API documentation (auto from Scramble)
├── MOBILE_GUIDELINES.md # Mobile-first design guidelines
└── DEPLOYMENT.md       # Deployment instructions
```

---

## 10. Git Workflow

### Branch Strategy

```
main           ── Production-ready code
├── develop    ── Integration branch
│   ├── feat/scraping-*
│   ├── feat/api-*
│   ├── feat/frontend-*
│   ├── feat/ml-*
│   └── fix/*
```

### Workflow per Task

```bash
# 1. Buat branch dari develop
git checkout develop
git pull origin develop
git checkout -b feat/api-patients

# 2. Kerjakan + commit
git add app/Http/Controllers/Api/PatientController.php
git commit -m "feat(api): add patient CRUD endpoints
- GET /api/patients (list with pagination)
- POST /api/patients (create with validation)
- GET /api/patients/{id} (detail with intakes)
- PUT /api/patients/{id} (update)
- DELETE /api/patients/{id} (soft delete)"

# 3. Push & buat PR
git push origin feat/api-patients
# → Buat Pull Request ke develop

# 4. Merge setelah review
git checkout develop
git merge feat/api-patients
git push origin develop
```

---

## 11. Commit Convention

```
Format:
<type>(<scope>): <subject>

<body> (opsional)

<footer> (opsional)
```

### Types & Examples

| Type | Example |
|------|---------|
| **feat** | `feat(api): add patient CRUD endpoints` |
| **fix** | `fix(mobile): bottom nav overlap on iPhone notch` |
| **ui** | `ui(calculator): redesign progress bar for mobile` |
| **api** | `api(auth): add google oauth callback endpoint` |
| **ml** | `ml(hybrid): add cold start strategy for new patients` |
| **scrape** | `scrape(tkpi): add 500 food entries from panganku` |
| **db** | `db(migration): add age_groups and maternal_statuses tables` |
| **docs** | `docs(readme): update API endpoints list` |
| **test** | `test(api): add patient feature tests with Pest` |
| **refactor** | `refactor(api): extract nutrition calculator service` |
| **perf** | `perf(db): add indexes for food search queries` |
| **ci** | `ci(actions): add automated test workflow` |
| **chore** | `chore(deps): update nuxt to 3.12` |

### Wajib:
- Setiap commit harus ada deskripsi (boleh Indonesia/Inggris)
- Body commit menjelaskan WHAT dan WHY, bukan HOW
- Satu commit = satu logical change

---

## 12. Directories Structure (Complete)

```
ujangnutree/
│
├── frontend/                          # Nuxt 3 Mobile-First SPA
│   ├── app/
│   │   ├── layouts/
│   │   │   └── default.vue           # BottomNav (mobile) + Sidebar (tablet+)
│   │   ├── pages/
│   │   │   ├── index.vue             # Dashboard
│   │   │   ├── sign-in.vue
│   │   │   ├── sign-up.vue
│   │   │   ├── forgot-password.vue
│   │   │   ├── reset-password.vue
│   │   │   ├── patients/
│   │   │   │   ├── index.vue         # List + pull-to-refresh
│   │   │   │   └── [id].vue          # Detail + tabs
│   │   │   ├── calculator/
│   │   │   │   ├── index.vue         # Calculator utama
│   │   │   │   └── [intakeId].vue    # Edit intake
│   │   │   ├── database/
│   │   │   │   ├── foods.vue         # Infinite scroll search
│   │   │   │   └── akg-profiles.vue  # AKG filterable list
│   │   │   ├── recipes/
│   │   │   │   ├── index.vue         # Grid cards
│   │   │   │   └── [id].vue          # Recipe detail
│   │   │   ├── settings/
│   │   │   │   ├── index.vue
│   │   │   │   ├── profile.vue
│   │   │   │   └── security.vue
│   │   │   └── send-feedback.vue
│   │   ├── components/
│   │   │   ├── ui/                   # shadcn-vue base
│   │   │   ├── layout/              # BottomNav, Sidebar, Header
│   │   │   ├── feature/             # FoodSearch, NutritionCard, dll
│   │   │   └── shared/              # EmptyState, ErrorState, etc
│   │   ├── composables/
│   │   │   ├── useApi.ts
│   │   │   ├── useAuth.ts
│   │   │   ├── useMobile.ts         # Mobile detection
│   │   │   └── useOffline.ts
│   │   ├── stores/
│   │   │   ├── auth.store.ts
│   │   │   ├── patient.store.ts
│   │   │   └── intake.store.ts
│   │   ├── i18n/
│   │   │   ├── id.json
│   │   │   └── en.json
│   │   └── middleware/
│   │       └── auth.ts
│   ├── public/
│   ├── app.vue
│   ├── nuxt.config.ts
│   ├── tailwind.config.ts
│   └── package.json
│
├── backend/                           # Laravel 11 API
│   ├── app/
│   │   ├── Http/
│   │   │   ├── Controllers/
│   │   │   │   └── Api/
│   │   │   │       ├── AuthController.php
│   │   │   │       ├── PatientController.php
│   │   │   │       ├── IntakeController.php
│   │   │   │       ├── FoodController.php
│   │   │   │       ├── RecipeController.php
│   │   │   │       ├── AkgProfileController.php
│   │   │   │       ├── FeedbackController.php
│   │   │   │       ├── DashboardController.php
│   │   │   │       └── SelectController.php
│   │   │   ├── Requests/
│   │   │   └── Resources/
│   │   ├── Models/
│   │   │   ├── User.php
│   │   │   ├── Patient.php
│   │   │   ├── Intake.php
│   │   │   ├── IntakeDetail.php
│   │   │   ├── Food.php
│   │   │   ├── Recipe.php
│   │   │   ├── RecipeFood.php
│   │   │   ├── AkgProfile.php
│   │   │   ├── AgeGroup.php
│   │   │   ├── MaternalStatus.php
│   │   │   ├── FoodCategory.php
│   │   │   └── Feedback.php
│   │   └── Services/
│   │       ├── NutritionCalculator.php
│   │       └── AkgCalculator.php
│   ├── database/
│   │   ├── migrations/
│   │   └── seeders/
│   │       ├── AgeGroupSeeder.php
│   │       ├── MaternalStatusSeeder.php
│   │       ├── FoodCategorySeeder.php
│   │       ├── AkgProfileSeeder.php
│   │       └── FoodSeeder.php
│   ├── routes/
│   │   └── api.php
│   ├── tests/
│   │   ├── Feature/
│   │   │   ├── AuthTest.php
│   │   │   ├── PatientTest.php
│   │   │   ├── IntakeTest.php
│   │   │   ├── FoodTest.php
│   │   │   ├── RecipeTest.php
│   │   │   └── AkgTest.php
│   │   └── Unit/
│   │       └── NutritionCalculatorTest.php
│   ├── Dockerfile
│   └── composer.json
│
├── ml-service/                        # Python FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── cbf.py               # Content-Based Filtering
│   │   │   ├── cf.py                # Collaborative Filtering
│   │   │   └── hybrid.py            # Hybrid Ensemble
│   │   ├── rules/
│   │   │   ├── __init__.py
│   │   │   └── constraints.py       # Allergen, diet, disease filters
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── recommendation.py
│   ├── training/
│   │   ├── train_pipeline.py
│   │   └── evaluate.py
│   ├── tests/
│   │   ├── test_recommender.py
│   │   ├── test_constraints.py
│   │   └── test_api.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── scraping/                          # Data Collection
│   ├── scripts/
│   │   ├── scrape_panganku.py
│   │   ├── scrape_usda.py
│   │   └── normalize.py
│   ├── output/
│   │   ├── raw/
│   │   ├── normalized/
│   │   └── final/
│   ├── logs/
│   └── README.md
│
├── database/                          # Database Schema
│   ├── schema.sql
│   ├── erd.md
│   └── seed/
│       └── foods_seed.csv
│
├── docs/
│   ├── PRD.md
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── MOBILE_GUIDELINES.md
│   └── DEPLOYMENT.md
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # Test on push & PR
│   │   └── deploy.yml                # Auto deploy to production
│   └── CODEOWNERS
│
├── docker-compose.yml
├── docker-compose.prod.yml
├── AGENTS.md
├── README.md
└── .gitignore
```

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/awaaaaja/UjangNutree.git
cd UjangNutree

# 2. Backend
cd backend
cp .env.example .env
composer install
php artisan key:generate
php artisan migrate --seed
php artisan serve

# 3. Frontend
cd frontend
npm install
npm run dev

# 4. ML Service
cd ml-service
pip install -r requirements.txt
uvicorn app.main:app --reload

# 5. Scraping
cd scraping
python scripts/scrape_panganku.py

# 6. Test
cd backend && php artisan test
cd frontend && npx playwright test
cd ml-service && pytest

# 7. Dokumentasi
git add docs/
git commit -m "docs(project): add PRD, architecture, and API documentation"

# 8. Deploy
git push origin main
```
