# AGENTS.md — UjangNutree

> Proyek rebuild Nutribase → **UjangNutree**
> GitHub: https://github.com/awaaaaja/UjangNutree

---

## Daftar Agent / Mode Eksekusi

Setiap task di bawah adalah mode/agent yang bisa kamu jalankan secara independen. Masing-masing punya prompt sendiri yang siap pakai.

---

## Agent 1: Inisialisasi Proyek & Repository

**Tujuan**: Setup project structure dan git repository.

```bash
# 1. Buat proyek
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/awaaaaja/UjangNutree.git
git push -u origin main

# 2. Setup struktur folder
ujangnutree/
├── frontend/          # Nuxt 3 / Next.js (mobile-first)
├── backend/           # Laravel API (Laravel 11)
├── ml-service/        # Python FastAPI (rekomendasi)
├── scraping/          # Script scraping data
├── database/          # Migrations, seeds, schema
├── docs/              # Dokumentasi
└── .github/           # CI/CD workflows
```

---

## Agent 2: Scraping & Dataset

**Prompt untuk dijalankan oleh agent code:**

```
Tugas: Scrape data komposisi pangan Indonesia dari sumber terbuka untuk database UjangNutree.

Sumber data target:
1. https://www.panganku.org/ — Database pangan Indonesia (TKPI)
2. https://fdc.nal.usda.gov/ — USDA FoodData Central API
3. Data BPOM RI — Produk pangan olahan (jika ada API publik)

Spesifikasi output:
- Format: JSON + CSV
- Minimal 2000+ entri makanan khas Indonesia
- Setiap entri memiliki: nama, kategori, energi (kcal), protein(g), lemak(g), karbohidrat(g), serat(g), takaran saji (gram)
- Include sumber data (source: 'tkpi' / 'usda' / 'manual')
- Simpan di folder /scraping/output/

Teknis:
- Gunakan Python (Scrapy/BeautifulSoup/requests)
- Handle rate limiting & retry
- Log setiap proses scraping ke /scraping/logs/
- Commit setiap batch dataset dengan pesan: "scrape: <sumber> — <jumlah> data"
- Dokumentasikan di /scraping/README.md

Pipeline:
scraping/
├── scripts/
│   ├── scrape_panganku.py
│   ├── scrape_usda.py
│   └── normalize.py
├── output/
│   ├── raw/           # Data mentah per sumber
│   ├── normalized/    # Data setelah normalisasi
│   └── final/         # Siap import ke database
├── logs/
└── README.md
```

---

## Agent 3: Setup Backend (Laravel 11 API)

**Prompt untuk agent code:**

```
Tugas: Buat REST API backend untuk UjangNutree menggunakan Laravel 11.

Spesifikasi:
- Autentikasi: Laravel Sanctum (SPA cookie-based) + Google OAuth
- Database: PostgreSQL dengan migrations lengkap
- API endpoints sesuai PRD (36+ endpoints): auth, patients, intakes, foods, recipes, akg, feedbacks, settings
- Full-text search menggunakan Meilisearch untuk tabel foods
- API documentation dengan Scramble
- Rate limiting, validation, error handling standar

Wajib:
- Database migrations & seeders
- Model relationships (User, Patient, Intake, IntakeDetail, Food, Recipe, RecipeFood, AkgProfile, dll)
- Resources/Transformers untuk response konsisten
- Form Request validation
- Repository/Service pattern untuk business logic
- Unit test dengan Pest PHP (minimal 70% coverage)
- Dockerfile untuk development

Commit convention:
- "feat(api): add <entity> CRUD endpoints"
- "feat(auth): add google oauth integration"
- "test(api): add <entity> feature tests"
- "docs(api): update scramble documentation"
```

---

## Agent 4: Setup Frontend (Mobile-First Nuxt 3 + Tailwind)

**Prompt untuk agent code:**

```
Tugas: Buat frontend UjangNutree dengan Nuxt 3, Vue 3 Composition API, Tailwind CSS, mobile-first design.

DESIGN SYSTEM — MOBILE FIRST:
- Base: 375px (mobile S) → 768px (tablet) → 1024px+ (desktop)
- Breakpoints: sm:640, md:768, lg:1024, xl:1280, 2xl:1536
- Touch-friendly: min target 44x44px untuk tap areas
- Bottom navigation untuk mobile (bukan sidebar)
- Swipe gestures untuk mobile (intake list, food search)
- Modal/drawer dari bawah untuk mobile (bottom sheet)
- Font: Inter atau Plus Jakarta Sans (modern, readable di mobile)

KOMPONEN WAJIB:
1. BottomNav (mobile) → Sidebar (tablet/desktop)
2. BottomSheet component (mobile) → Dialog (tablet/desktop)
3. Responsive DataTable → Card grid di mobile
4. SearchBar dengan voice input fallback
5. Skeleton loading untuk semua halaman
6. Pull-to-refresh untuk list pages
7. Swipeable card untuk intake list

HALAMAN (18 routes — MOBILE FIRST):
1. / — Dashboard mobile (KPI cards stacked vertikal)
2. /sign-in, /sign-up — Full-screen mobile forms
3. /patients — Card list mobile, swipe to delete
4. /patients/:id — Tab layout (info, intakes, charts)
5. /calculator — Sticky bottom input, scrollable results
6. /database/foods — Search bar fixed top, infinite scroll
7. /recipes — Grid cards 2 kolom mobile, 3 kolom tablet
8. /settings — Native-style list items

TEKNIS:
- Tailwind CSS utility-first (NO Element Plus atau library UI berat)
- shadcn-vue atau Headless UI untuk komponen aksesibel
- Pinia untuk state management
- Nuxt i18n (id + en)
- PWA support (manifest, service worker, offline fallback)
- nuxt/image untuk optimasi gambar
- nuxt/icon untuk icon

Commit convention:
- "feat(ui): add <component> mobile-first"
- "feat(page): add <route> page responsive"
- "fix(ui): mobile layout <issue>"
- "style(ui): refine <breakpoint> responsive"
```

---

## Agent 5: ML Recommendation Service (Python FastAPI)

**Prompt untuk agent code:**

```
Tugas: Buat microservice ML untuk meal recommendation system UjangNutree.

Arsitektur:
- Python 3.11+ FastAPI
- scikit-learn untuk model
- PostgreSQL pgvector untuk vector similarity
- Redis untuk cache rekomendasi
- MLflow untuk model tracking

Endpoint:
POST /api/v1/recommend/meals
{
    "patient_id": "uuid",
    "context": {
        "meal_type": "breakfast|lunch|dinner|snack",
        "target_energy_kcal": 450,
        "target_protein_g": 20,
        "preferences": ["low_carb"],
        "allergies": ["seafood"],
        "max_results": 5
    }
}

Implementasi 3 pendekatan:
1. Content-Based Filtering (cosine similarity on nutritional profiles)
2. Collaborative Filtering (SVD matrix factorization)
3. Hybrid ensemble (CBF 40% + CF 40% + Rule-based 20%)

Rule engine constraints:
- Allergen filter (hard constraint)
- Diet preference filter
- Medical condition compatibility (diabetes, hipertensi, CKD, dll)
- Meal type appropriateness

Cold start strategy:
- New patient: based on AKG target + demography
- New food: CBF only
- Sparse data: weight CBF > CF

Setup:
ml-service/
├── app/
│   ├── main.py
│   ├── models/
│   │   ├── cbf.py
│   │   ├── cf.py
│   │   └── hybrid.py
│   ├── rules/
│   │   └── constraints.py
│   ├── api/
│   │   └── routes.py
│   └── schemas/
│       └── recommendation.py
├── training/
│   ├── train_pipeline.py
│   └── evaluate.py
├── Dockerfile
└── requirements.txt
```

---

## Agent 6: Frontend — Implementasi Halaman

**Prompt untuk agent code:**

```
Tugas: Implementasi setiap halaman UjangNutree dengan mobile-first design.

URUTAN PRIORITAS IMPLEMENTASI:

Phase 1 — Auth & Layout (done = tandai [x])
[x] Layout utama (BottomNav mobile, Sidebar tablet/desktop)
[x] Sign-in page (mobile-optimized form)
[x] Sign-up page
[x] Forgot/reset password
[x] Google OAuth callback

Phase 2 — Core Features
[ ] Dashboard — 4 KPI cards + chart intake mingguan
[ ] Patients list — card layout mobile, pull-to-refresh
[ ] Patient detail — tab: profile, intakes, charts
[ ] Create/Edit patient form — bottom sheet mobile

Phase 3 — Calculator
[ ] Calculator page — search makanan (sticky search bar)
[ ] Intake form — tambah makanan dengan porsi
[ ] Hasil kalkulasi — visual progress bar vs AKG target
[ ] Lock/Cancel intake

Phase 4 — Database
[ ] Food database — infinite scroll, search with Meilisearch
[ ] Food detail — nutrisi card
[ ] AKG profiles list — filterable
[ ] Recipes list — grid responsive

Phase 5 — Settings
[ ] Profile settings
[ ] Security/password
[ ] Feedback form

MOBILE UX CHECKLIST tiap halaman:
□ Touch targets ≥ 44px
□ Bottom sheet instead of modal (mobile)
□ Native-like scrolling behavior
□ Pull-to-refresh
□ Skeleton loading
□ Empty state illustration
□ Error state with retry button
□ Network indicator (offline detection)
```

---

## Agent 7: Dokumentasi & Git Workflow

**Commit Convention:**

```
<type>(<scope>): <description>

Types:
feat     — Fitur baru
fix      — Bug fix
ui       — Perubahan UI/UX
api      — Perubahan API
ml       — Perubahan ML service
scrape   — Data scraping
db       — Database migration/seed
docs     — Dokumentasi
test     — Testing
refactor — Refactoring kode
perf     — Performance improvement
ci       — CI/CD changes
chore    — Lainnya

Scope examples: auth, patients, foods, calculator, mobile, tablet

Wajib: Setiap commit harus ada deskripsi singkat (bahasa Indonesia atau Inggris).
Contoh:
  feat(auth): add google oauth login
  ui(mobile): fix bottom nav overlap on iPhone X
  scrape(tkpi): add 500 food entries from panganku
  docs(readme): update API endpoints list
```

---

## Agent 8: Testing & Quality Assurance

**Prompt untuk agent code:**

```
Tugas: Setup dan implementasi testing untuk seluruh stack UjangNutree.

Backend (Laravel — Pest PHP):
wajib/
├── Feature/
│   ├── AuthTest.php
│   ├── PatientTest.php
│   ├── IntakeTest.php
│   ├── FoodTest.php
│   ├── RecipeTest.php
│   └── AkgTest.php
├── Unit/
│   └── NutritionCalculatorTest.php
└── Pest.php

Frontend (Playwright — E2E):
wajib/
├── e2e/
│   ├── auth.spec.ts
│   ├── patient.spec.ts
│   ├── calculator.spec.ts
│   └── mobile-responsive.spec.ts
├── unit/
│   └── components/ (Vitest)
└── playwright.config.ts

ML Service (pytest):
wajib/
├── test_recommender.py
├── test_constraints.py
└── test_api.py

Target coverage: Backend 80%, Frontend 70%, ML 80%
CI: GitHub Actions — auto-run tests on push & PR
```

---

## Ringkasan Command Line

```bash
# Clone & start
git clone https://github.com/awaaaaja/UjangNutree.git
cd UjangNutree

# Backend
cd backend && cp .env.example .env
composer install
php artisan migrate --seed
php artisan serve

# Frontend
cd frontend && npm install
npm run dev

# ML Service
cd ml-service && pip install -r requirements.txt
uvicorn app.main:app --reload

# Scraping
cd scraping && python scripts/scrape_panganku.py

# Test all
cd backend && php artisan test
cd frontend && npx playwright test
cd ml-service && pytest
```
