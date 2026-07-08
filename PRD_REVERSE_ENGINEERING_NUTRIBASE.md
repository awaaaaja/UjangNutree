# PRD & Reverse Engineering Report: Nutribase by Nutrisee

## 📋 Daftar Isi

1. [Ringkasan Eksekutif](#1-ringkasan-eksekutif)
2. [Hasil Reverse Engineering](#2-hasil-reverse-engineering)
3. [Dataset & Plan Scraping](#3-dataset--plan-scraping)
4. [Arsitektur Sistem](#4-arsitektur-sistem)
5. [App Flow](#5-app-flow)
6. [ERD (Entity Relationship Diagram)](#6-erd)
7. [Flowchart](#7-flowchart)
8. [PRD (Product Requirements Document)](#8-prd)
9. [Rencana Rebuild](#9-rencana-rebuild)

---

## 1. Ringkasan Eksekutif

**Nutribase** adalah platform database gizi berbasis web yang dikembangkan oleh **Nutrisee.ID** — sebuah ekosistem edukasi gizi di Indonesia. Aplikasi ini memungkinkan ahli gizi/dietisien untuk mengelola data pasien, menghitung asupan gizi, mengelola resep, dan mengakses database makanan serta profil AKG (Angka Kecukupan Gizi).

### Ekosistem Nutrisee
| Produk | URL | Tujuan |
|--------|-----|--------|
| **Nutrisee** (Utama) | https://www.nutrisee.id/ | Platform edukasi & bimbingan gizi (React) |
| **Nutribase** | https://nutribase.nutrisee.id/ | Database & kalkulator gizi (Nuxt 3) |
| **API Nutribase** | https://api-nutribase.nutrisee.id/ | Backend API (Laravel) |
| **NutriSee Mobile** | GitHub: NutriSee-ID | Aplikasi mobile scoring gizi (Bangkit) |

### Tech Stack Teridentifikasi

| Layer | Teknologi |
|-------|-----------|
| **Frontend** | Nuxt 3 (Vue 3.5.21), Vite, Vue Router 4.5 |
| **UI Library** | Element Plus (el-button, el-dialog, el-select, el-table, dll) |
| **State Management** | Pinia |
| **i18n** | vue-i18n 10.0.8 (Indonesia & Inggris) |
| **Icons** | Iconify (~200 icon sets) |
| **HTTP Client** | Custom `$api()` wrapper (Nuxt $fetch) |
| **Backend** | Laravel (Sanctum auth, Scramble API docs) |
| **Realtime** | Laravel Reverb (WebSocket) |
| **Auth** | Email/password + Google OAuth |

---

## 2. Hasil Reverse Engineering

### 2.1 Page Routes (18 Routes)

| Route Name | Path | Deskripsi |
|-----------|------|-----------|
| `index` | `/` | Dashboard utama |
| `sign-in` | `/sign-in` | Halaman login |
| `sign-up` | `/sign-up` | Halaman registrasi |
| `forgot-password` | `/forgot-password` | Lupa password |
| `reset-password` | `/reset-password/:token/:email` | Reset password |
| `patients` | `/patients` | Daftar pasien |
| `patients-id` | `/patients/:id` | Detail pasien |
| `patients-id-intakeId` | `/patients/:id/:intakeId` | Intake pasien |
| `recipes` | `/recipes` | Daftar resep |
| `recipes-id` | `/recipes/:id` | Detail resep |
| `calculator` | `/calculator` | Kalkulator gizi |
| `calculator-intakeId` | `/calculator/:intakeId` | Kalkulator untuk intake tertentu |
| `database-foods` | `/database/foods` | Database makanan |
| `database-akg-profiles` | `/database/akg-profiles` | Database profil AKG |
| `settings` | `/settings` | Pengaturan |
| `settings-profile` | `/settings/profile` | Edit profil |
| `settings-security` | `/settings/security` | Keamanan/password |
| `send-feedback` | `/send-feedback` | Kirim feedback |

### 2.2 API Endpoints (36+ Endpoints)

#### Auth
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | `/api/csrf` | CSRF token (Sanctum) |
| GET | `/api/auth/client-check` | Cek autentikasi |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/register` | Register |
| POST | `/api/auth/login/google` | Google OAuth |
| POST | `/api/auth/logout` | Logout |
| POST | `/api/auth/forgot-password` | Lupa password |
| POST | `/api/auth/reset-password` | Reset password |
| PUT | `/api/auth/user/password` | Ubah password |
| PUT | `/api/auth/user/profile-information` | Update profil |

#### Dashboard
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | `/api/dashboard/total-patients` | Total pasien |
| GET | `/api/dashboard/total-calculations` | Total kalkulasi |

#### Patients
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET/POST | `/api/patients` | List/Create pasien |
| GET/PUT/DELETE | `/api/patients/{id}` | Single CRUD pasien |
| GET/POST | `/api/patients/{id}/intakes` | List/Create intake |
| GET/PUT | `/api/patients/{id}/intakes/{id}` | Single CRUD intake |
| DELETE | `/api/patients/{id}/intakes/{id}` | Hapus intake |

#### Intakes
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET/PUT | `/api/intakes/{id}` | Update intake |
| DELETE | `/api/intakes/{id}` | Hapus intake |
| POST | `/api/intakes/{id}/snapshots` | Simpan snapshot |
| PATCH | `/api/intakes/{id}/lock` | Lock intake |
| PATCH | `/api/intakes/{id}/cancel` | Cancel intake |
| DELETE | `/api/intakes/{id}/details/{id}` | Hapus detail intake |
| POST | `/api/intakes/{id}/calculate-akg` | Hitung AKG |

#### Recipes
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET/POST | `/api/recipes` | List/Create resep |
| GET/PUT/DELETE | `/api/recipes/{id}` | Single CRUD resep |
| POST | `/api/recipes/{id}/foods` | Tambah makanan ke resep |
| GET/PUT/DELETE | `/api/recipes/{id}/foods/{id}` | CRUD makanan di resep |

#### Foods & Nutrients
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET/POST | `/api/foods` | List/Create makanan |
| GET | `/api/nutrients` | List nutrient |

#### Reference/Select
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | `/api/select/foods` | Options makanan |
| GET | `/api/select/patients` | Options pasien |
| GET | `/api/select/age-groups` | Options kelompok umur |
| GET | `/api/select/maternal-statuses` | Options status maternal |
| GET | `/api/select/recipes` | Options resep |

#### AKG
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET | `/api/akg-profiles` | List profil AKG |

#### Feedback & Settings
| Method | Endpoint | Fungsi |
|--------|----------|--------|
| GET/POST | `/api/feedbacks` | List/Create feedback |
| GET/PUT | `/api/feedbacks/{id}` | Single CRUD feedback |
| DELETE | `/api/feedbacks/{id}` | Hapus feedback |
| GET/PUT | `/api/settings/contact-number` | Setting kontak |

---

## 3. Dataset & Plan Scraping

### 3.1 Sumber Data yang Teridentifikasi

| Dataset | Sumber | Format | Status |
|---------|--------|--------|--------|
| **TKPI** (Tabel Komposisi Pangan Indonesia) | Kemenkes RI | Terintegrasi di database | ✅ Ada |
| **Resep RS RSCM** | RSUPN Dr. Cipto Mangunkusumo | Data manual tim Nutrisee | ✅ Ada |
| **Resep RS Dr. Kariadi** | RSUP Dr. Kariadi Semarang | Data manual tim Nutrisee | ✅ Ada |
| **Input Manual Ahli Gizi** | Tim Nutrisee | Data harian | ✅ Ada |
| **Data Makanan Brand/Produk** | Database internal | Manual entry | ✅ Ada |

### 3.2 Plan Scraping & Pengumpulan Data

#### Fase 1: Scraping Sumber Terbuka
```
Target Scraping:
├── https://www.panganku.org/ (Database pangan Indonesia)
├── https://fdc.nal.usda.gov/ (USDA Food Data Central)
├── Data BPOM RI (produk pangan olahan)
└── API publik pemerintah terkait gizi

Tools: Python (Scrapy/Selenium/BeautifulSoup)
Output: Raw CSV/JSON → Normalisasi → Import ke DB
```

#### Fase 2: Enrichment Data Internal
```
Sumber Data Internal:
├── Data historis intake pasien (anonim)
├── Database resep RS mitra
├── Data feedback user → improvement dataset
└── User-generated recipes (dengan validasi ahli)

Pipeline:
Raw Data → Cleaning → Normalisasi Gizi → Validasi Ahli → Production DB
```

#### Fase 3: API External Integration
```
Integrasi API:
├── USDA FoodData Central API
├── Open Food Facts API
├── Data BPS (Badan Pusat Statistik) pola konsumsi
└── Jurnal/penelitian gizi terbaru
```

### 3.3 Skema Data Makanan (Food Schema)
```
Food {
  id: UUID
  name: String (e.g., "Nasi Putih")
  category_id: FK -> food_categories
  brand: String (nullable)
  serving_size: Float (gram)
  serving_unit: String (e.g., "gram", "porsi")
  energy_kcal: Float
  protein_g: Float
  fat_g: Float
  carbohydrate_g: Float
  fiber_g: Float
  water_g: Float
  ash_g: Float
  source: ENUM('tkpi', 'manual', 'rumah_sakit', 'usda', 'brand')
  verification_status: ENUM('draft', 'verified', 'need_review')
  created_by: FK -> users
  metadata: JSON (additional nutrients, references)
}
```

### 3.4 Nutrisi yang Dilacak (23+ Nutrisi)
```
Makronutrien: Energi (kcal), Protein, Lemak, Karbohidrat, Serat, Air, Abu
Vitamin: A, D, E, K, C, B1, B2, B3, B5, B6, B9, B12
Mineral: Kalsium, Fosfor, Kalium, Natrium, Magnesium, Besi, Zink, Yodium, Selenium, Mangan, Tembaga
```

---

## 4. Arsitektur Sistem

### 4.1 Arsitektur High-Level

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLOUD INFRASTRUCTURE                          │
│                                                                      │
│  ┌──────────────────┐    ┌──────────────────┐                       │
│  │   Nutrisee Web   │    │   Nutribase App  │                       │
│  │ (React + Vite)   │    │ (Nuxt 3 + Vue 3) │                       │
│  │  nutrisee.id     │    │ nutribase.nutri  │                       │
│  └───────┬──────────┘    └────────┬─────────┘                       │
│          │                        │                                  │
│          │                        │                                  │
│  ┌───────┴────────────────────────┴─────────┐                       │
│  │          API GATEWAY (Laravel)             │                       │
│  │     api-nutribase.nutrisee.id             │                       │
│  │                                            │                       │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐  │                       │
│  │  │ Auth API │ │PatientAPI│ │ Food API │  │                       │
│  │  │ Sanctum  │ │ RESTful  │ │ RESTful  │  │                       │
│  │  └──────────┘ └──────────┘ └──────────┘  │                       │
│  └────────────────────┬──────────────────────┘                       │
│                       │                                              │
│  ┌────────────────────┴──────────────────────┐                       │
│  │           DATABASE LAYER                    │                       │
│  │  ┌─────────────┐  ┌──────────────────┐    │                       │
│  │  │   MySQL/     │  │   Redis Cache    │    │                       │
│  │  │  PostgreSQL  │  │  (Session,Queue) │    │                       │
│  │  └─────────────┘  └──────────────────┘    │                       │
│  └────────────────────────────────────────────┘                       │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │              REALTIME (Laravel Reverb)                        │    │
│  │         wss://ws-nutribase.nutrisee.id:443                   │    │
│  └─────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

### 4.2 Arsitektur Frontend (Nuxt 3)

```
src/
├── pages/                          # File-based routing
│   ├── index.vue                   # Dashboard
│   ├── sign-in.vue                 # Login
│   ├── sign-up.vue                 # Register
│   ├── forgot-password.vue         # Lupa password
│   ├── reset-password.vue          # Reset password
│   ├── patients/
│   │   ├── index.vue               # List pasien
│   │   └── [id].vue                # Detail & intake pasien
│   ├── recipes/
│   │   ├── index.vue               # List resep
│   │   └── [id].vue                # Detail resep
│   ├── calculator/
│   │   ├── index.vue               # Kalkulator utama
│   │   └── [intakeId].vue          # Kalkulator per intake
│   ├── database/
│   │   ├── foods.vue               # Database makanan
│   │   └── akg-profiles.vue        # Profil AKG
│   ├── settings/
│   │   ├── index.vue               # Pengaturan utama
│   │   ├── profile.vue             # Edit profil
│   │   └── security.vue            # Keamanan
│   └── send-feedback.vue           # Feedback
│
├── composables/                    # Shared logic
│   └── api.js                      # $api wrapper
│
├── stores/                         # Pinia stores
│   ├── auth.store.js
│   ├── patient.store.js
│   └── ...
│
├── i18n/
│   ├── id.json                     # Bahasa Indonesia
│   └── en.json                     # English
│
└── layouts/
    └── default.vue                 # Layout utama
```

### 4.3 Arsitektur Backend (Laravel)

```
app/
├── Http/
│   ├── Controllers/
│   │   ├── Api/
│   │   │   ├── AuthController.php
│   │   │   ├── PatientController.php
│   │   │   ├── IntakeController.php
│   │   │   ├── RecipeController.php
│   │   │   ├── FoodController.php
│   │   │   ├── NutrientController.php
│   │   │   ├── AkgProfileController.php
│   │   │   ├── FeedbackController.php
│   │   │   ├── DashboardController.php
│   │   │   └── SelectController.php
│   │   └── ...
│   ├── Middleware/
│   │   └── ...
│   └── Requests/
│       └── ...
├── Models/
│   ├── User.php
│   ├── Patient.php
│   ├── Intake.php
│   ├── IntakeDetail.php
│   ├── Food.php
│   ├── Recipe.php
│   ├── RecipeFood.php
│   ├── Nutrient.php
│   ├── AkgProfile.php
│   ├── AgeGroup.php
│   ├── MaternalStatus.php
│   ├── FoodCategory.php
│   └── Feedback.php
├── Services/
│   ├── NutritionCalculatorService.php
│   └── AkgCalculationService.php
└── ...
```

---

## 5. App Flow

### 5.1 User Journey Map

```
                    ┌──────────────┐
                    │  Landing     │
                    │  Page        │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Sign In /   │
                    │  Register    │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
       ┌──────▼─────┐ ┌───▼────┐ ┌────▼──────┐
       │ Dashboard  │ │ Pasien │ │ Resep     │
       │ (Home)     │ │ Mgmt   │ │ Mgmt      │
       └──────┬─────┘ └───┬────┘ └────┬──────┘
              │            │           │
       ┌──────▼─────┐ ┌───▼────┐      │
       │ Stats      │ │ Intake │      │
       │ Overview   │ │ Record │      │
       └────────────┘ └───┬────┘      │
                          │           │
                   ┌──────▼─────┐ ┌───▼────────┐
                   │ Kalkulator │ │ Database   │
                   │ Gizi + AKG │ │ Makanan &  │
                   └──────┬─────┘ │ AKG        │
                          │       └────────────┘
                          │
                   ┌──────▼─────┐
                   │ Hasil      │
                   │ Perhitungan│
                   │ (Snapshot) │
                   └────────────┘
```

### 5.2 Alur Login

```
User ──► /sign-in
          │
          ├──► Email/Password ──► POST /api/auth/login
          │                          │
          │                     ┌────▼────┐
          │                     │ Sanctum │
          │                     │ Session │
          │                     └────┬────┘
          │                          │
          ├──► Google OAuth ──► POST /api/auth/login/google
          │                          │
          │                     ┌────▼────┐
          │                     │ OAuth   │
          │                     │ Callback│
          │                     └────┬────┘
          │                          │
          ├──► Lupa Password ──► POST /api/auth/forgot-password
          │                          │
          │                     ┌────▼────┐
          │                     │ Email   │
          │                     │ Reset   │
          │                     │ Link    │
          │                     └────┬────┘
          │                          │
          │                    ┌─────▼──────┐
          │                    │ Reset Form │
          │                    │ (/reset-   │
          │                    │ password/) │
          │                    └─────┬──────┘
          │                          │
          │                    POST /api/auth/reset-password
          │                          │
          └──────► Redirect ke Dashboard
```

### 5.3 Alur Manajemen Pasien & Intake

```
Dashboard
    │
    ▼
[Patients List] ──► GET /api/patients
    │
    ├── [Create Patient] ──► POST /api/patients
    │       │
    │       ▼
    │   [Patient Detail Page]
    │       │
    │       ├── [Edit] ──► PUT /api/patients/{id}
    │       │
    │       └── [Delete] ──► DELETE /api/patients/{id}
    │
    └── [Select Patient] ──► GET /api/patients/{id}
            │
            ▼
    [Patient Detail + Intakes]
            │
            ├── [New Intake] ──► POST /api/patients/{id}/intakes
            │       │
            │       ▼
            │   [Calculator Page]
            │       │
            │       ├── [Add Food] ──► Search /api/select/foods?q=
            │       │       │
            │       │       ▼
            │       │   [Portion Input] ──► POST /api/intakes/{id}/details
            │       │
            │       ├── [Calculate AKG] ──► POST /api/intakes/{id}/calculate-akg
            │       │
            │       ├── [Save Snapshot] ──► POST /api/intakes/{id}/snapshots
            │       │
            │       ├── [Lock Intake] ──► PATCH /api/intakes/{id}/lock
            │       │
            │       └── [Cancel Intake] ──► PATCH /api/intakes/{id}/cancel
            │
            └── [View Intake] ──► GET /api/intakes/{id}
```

### 5.4 Alur Database Makanan & Resep

```
[Daftar Makanan]
    │
    ├── Food Database (/database/foods)
    │       │
    │       ├── [Browse] ──► GET /api/foods?search=&category=&page=
    │       │
    │       ├── [Create Food] ──► POST /api/foods
    │       │
    │       └── [View/Edit] ──► GET/PUT /api/foods/{id}
    │
    ├── AKG Profiles (/database/akg-profiles)
    │       │
    │       └── [Browse] ──► GET /api/akg-profiles?age_group=&gender=
    │
    └── [Resep]
            │
            ├── Recipe List ──► GET /api/recipes
            │
            ├── [Create Recipe] ──► POST /api/recipes
            │       │
            │       └── [Add Foods] ──► POST /api/recipes/{id}/foods
            │
            └── [View/Edit] ──► GET/PUT /api/recipes/{id}
```

---

## 6. ERD (Entity Relationship Diagram)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ENTITY RELATIONSHIP DIAGRAM                        │
│                                                                              │
│  ┌──────────────┐       ┌──────────────────┐       ┌──────────────────┐     │
│  │    users     │       │    patients      │       │     intakes      │     │
│  ├──────────────┤       ├──────────────────┤       ├──────────────────┤     │
│  │ id (PK)      │1──N→  │ id (PK)          │1──N→  │ id (PK)          │     │
│  │ name         │       │ user_id (FK)     │       │ patient_id (FK)  │     │
│  │ email        │       │ name             │       │ date             │     │
│  │ password     │       │ birth_date       │       │ meal_type        │     │
│  │ role         │       │ gender           │       │ status (lock/   │     │
│  │ profile_photo│       │ weight           │       │         cancel)  │     │
│  │ phone        │       │ height           │       │ notes            │     │
│  │ created_at   │       │ maternal_status  │       │ created_at       │     │
│  └──────────────┘       │ age_group_id (FK)│       └────────┬─────────┘     │
│                          └──────────────────┘                │              │
│                              │                               │              │
│                              │                               │ 1            │
│                              │                               │              │
│                              │                      ┌───────┴────────┐     │
│                              │                      │ intake_details │     │
│                              │                      ├────────────────┤     │
│                              │                      │ id (PK)        │     │
│                              │                      │ intake_id (FK) │     │
│                              │                      │ food_id (FK)   │     │
│                              │                      │ portion_size   │     │
│                              │                      │ portion_unit   │     │
│                              │                      │ calculated_*   │     │
│                              │                      └───────┬────────┘     │
│                              │                              │              │
│  ┌──────────────┐            │                              │ N            │
│  │  age_groups  │            │                              │              │
│  ├──────────────┤            │              ┌───────────────┴──────┐       │
│  │ id (PK)      │◄───────────┘              │       foods         │       │
│  │ name         │                            ├────────────────────┤       │
│  │ min_age      │                            │ id (PK)            │       │
│  │ max_age      │                            │ name               │       │
│  └──────────────┘                            │ category_id (FK)   │       │
│                                              │ brand              │       │
│  ┌────────────────────┐                      │ serving_size       │       │
│  │ maternal_statuses  │                      │ serving_unit       │       │
│  ├────────────────────┤                      │ energy_kcal        │       │
│  │ id (PK)            │                      │ protein_g          │       │
│  │ name               │                      │ fat_g              │       │
│  │ description        │                      │ carbohydrate_g     │       │
│  └────────────────────┘                      │ fiber_g            │       │
│                                              │ water_g            │       │
│  ┌──────────────────┐                        │ source             │       │
│  │  akg_profiles    │◄───(reference)──┐      │ verification_status│       │
│  ├──────────────────┤                 │      │ created_by (FK)    │       │
│  │ id (PK)          │                 │      └────────┬───────────┘       │
│  │ name             │                 │               │                   │
│  │ age_group_id (FK)│                 │               │                   │
│  │ gender           │                 │               │                   │
│  │ maternal_status  │                 │               │ N                 │
│  │ energy_target    │                 │               │                   │
│  │ protein_target   │     ┌───────────┴───────────────┴──────┐            │
│  │ fat_target       │     │         nutrients                │            │
│  │ ...              │     ├──────────────────────────────────┤            │
│  └──────────────────┘     │ id (PK)                          │            │
│                           │ name                             │            │
│  ┌──────────────────┐     │ unit                             │            │
│  │  food_categories │     │ category (macro/vitamin/mineral) │            │
│  ├──────────────────┤     └──────────────────────────────────┘            │
│  │ id (PK)          │                                                      │
│  │ name             │     ┌──────────────────┐       ┌──────────────────┐  │
│  │ parent_id (FK)   │     │    recipes       │       │  recipe_foods    │  │
│  └──────────────────┘     ├──────────────────┤       ├──────────────────┤  │
│                           │ id (PK)          │1──N→  │ id (PK)          │  │
│  ┌──────────────────┐     │ user_id (FK)     │       │ recipe_id (FK)   │  │
│  │    feedbacks     │     │ name             │       │ food_id (FK)     │  │
│  ├──────────────────┤     │ description      │       │ amount           │  │
│  │ id (PK)          │     │ servings         │       │ unit             │  │
│  │ user_id (FK)     │     │ instructions     │       └──────────────────┘  │
│  │ message          │     │ created_at       │                             │
│  │ rating           │     └──────────────────┘                             │
│  │ status           │                                                      │
│  └──────────────────┘                                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Relasi Kunci:
- **users 1──N patients** (Satu user punya banyak pasien)
- **patients 1──N intakes** (Satu pasien punya banyak record intake)
- **intakes 1──N intake_details** (Satu intake punya banyak makanan)
- **foods 1──N intake_details** (Satu makanan bisa dipake banyak intake)
- **age_groups 1──N patients** (Kelompok umur referensi pasien)
- **users 1──N recipes** (Satu user punya banyak resep)
- **recipes N──M foods via recipe_foods** (Resep terdiri dari banyak makanan)
- **users 1──N feedbacks** (Satu user punya banyak feedback)
- **food_categories 1──N foods** (Kategori makanan)

---

## 7. Flowchart

### 7.1 Flowchart Autentikasi

```
                    ┌─────────────────────┐
                    │   START             │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Buka Website      │
                    │ nutribase.nutrisee  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Cek Session       │
                    │ GET /api/auth/      │
                    │ client-check        │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                 Sudah Login          Belum Login
                    │                     │
                    ▼                     ▼
            ┌──────────────┐    ┌─────────────────────┐
            │ Redirect ke  │    │   Tampilkan Halaman  │
            │ Dashboard    │    │   Sign In            │
            └──────────────┘    └──────────┬──────────┘
                                           │
                              ┌────────────┼────────────┐
                              │            │            │
                              ▼            ▼            ▼
                      ┌────────────┐ ┌──────────┐ ┌──────────┐
                      │Login Email │ │Google    │ │Register  │
                      │/Password   │ │OAuth     │ │          │
                      └─────┬──────┘ └────┬─────┘ └────┬─────┘
                            │             │            │
                            ▼             ▼            │
                    ┌──────────────┐ ┌──────────┐      │
                    │ POST /api/   │ │Redirect  │      │
                    │ auth/login   │ │ ke Google│      │
                    └──────┬───────┘ └────┬─────┘      │
                           │              │            │
                           ▼              ▼            │
                     ┌──────────┐  ┌──────────┐       │
                     │Validasi  │  │Callback  │       │
                     │Credential│  │ + Login  │       │
                     └────┬─────┘  └────┬─────┘       │
                          │             │             │
                     ┌────┴────┐        │             │
                     │         │        │             │
                   Valid    Invalid     │             │
                     │         │        │             │
                     ▼         ▼        │             │
              ┌──────────┐ ┌──────┐     │             │
              │Set       │ │Error │     │             │
              │Session   │ │Msg   │     │             │
              └────┬─────┘ └──────┘     │             │
                   │         │          │             │
                   └────┬────┘          │             │
                        │               │             │
                        ▼               ▼             ▼
                    ┌──────────────────────────────┐
                    │      Redirect ke Dashboard   │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                            ┌──────────────┐
                            │     END      │
                            └──────────────┘
```

### 7.2 Flowchart Kalkulasi Gizi

```
                    ┌─────────────────────┐
                    │   START             │
                    │   (Pilih Pasien +   │
                    │    Buat Intake)     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Tampilkan Form    │
                    │   Intake Baru       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Input Data Pasien │
                    │   (BB, TB, Usia,    │
                    │    Gender, Status)  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Cari & Tambah     │
                    │   Makanan           │
                    │   (Search Food DB)  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Input Porsi       │
                    │   (Gram/Ukuran)     │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
              Tambah Lagi?            Selesai
                    │                     │
                    └───→ (loop)          ▼
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Hitung Total Gizi │
                    │   (Energi, Protein, │
                    │    Lemak, KH, dll)  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Hitung AKG        │
                    │   POST /api/intakes │
                    │   /{id}/calculate-  │
                    │   akg               │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Tampilkan Hasil   │
                    │   ┌───────────────┐ │
                    │   │ Total Asupan  │ │
                    │   │ vs AKG Target │ │
                    │   │ Persentase    │ │
                    │   │ Kecukupan     │ │
                    │   │ Grafik/Chart  │ │
                    │   └───────────────┘ │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                 Simpan               Lock/
                Snapshot             Cancel Intake
                    │                     │
                    ▼                     ▼
            ┌──────────────┐     ┌──────────────┐
            │POST /api/    │     │PATCH /api/   │
            │intakes/{id}/ │     │intakes/{id}/ │
            │snapshots     │     │lock | cancel │
            └──────┬───────┘     └──────┬───────┘
                   │                    │
                   ▼                    ▼
            ┌──────────────┐    ┌──────────────┐
            │  Sukses      │    │  Status      │
            │  Tersimpan   │    │  Terupdate   │
            └──────┬───────┘    └──────┬───────┘
                   │                    │
                   └────────┬───────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │    END       │
                     │ (Redirect ke │
                     │ Detail       │
                     │ Pasien)      │
                     └──────────────┘
```

### 7.3 Flowchart CRUD Pasien

```
                    ┌─────────────────────┐
                    │   START             │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Halaman Daftar    │
                    │   Pasien            │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │ Tambah       │ │ Pilih Pasien │ │ Cari/Search  │
      │ Pasien Baru  │ │ (Lihat       │ │ Pasien       │
      └──────┬───────┘ │ Detail)      │ └──────────────┘
             │         └──────┬───────┘
             ▼                │
      ┌──────────────┐       ▼
      │ Form Input   │ ┌──────────────┐
      │ Nama, Usia,  │ │ Detail       │
      │ BB, TB,      │ │ Pasien +     │
      │ Gender       │ │ Riwayat      │
      └──────┬───────┘ │ Intake       │
             │         └──────┬───────┘
             ▼                │
      POST /api/      ┌───────┼───────┐
      patients        │       │       │
             │        ▼       ▼       ▼
             │    ┌─────┐ ┌─────┐ ┌─────┐
             │    │Edit │ │Intake│ │Hapus│
             │    └──┬──┘ └─────┘ └──┬──┘
             │       │               │
             │       ▼               ▼
             │  PUT /api/      DELETE /api/
             │  patients/{id}  patients/{id}
             │       │               │
             └───┬───┘               │
                 │                   │
                 ▼                   ▼
          ┌──────────────┐   ┌──────────────┐
          │ Refresh      │   │ Konfirmasi   │
          │ Daftar       │   │ Hapus        │
          └──────────────┘   └──────────────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │   END        │
                              └──────────────┘
```

---

## 8. PRD (Product Requirements Document)

### 8.1 Vision & Mission

**Vision**: Menjadi platform database gizi nomor satu di Indonesia yang membantu para profesional kesehatan dalam memberikan pelayanan gizi terbaik.

**Mission**:
1. Menyediakan database komposisi pangan Indonesia terlengkap dan terverifikasi
2. Memudahkan kalkulasi gizi dan AKG untuk kebutuhan klinis
3. Mendukung digitalisasi rekam medis gizi di Indonesia
4. Menjadi referensi terpercaya untuk data gizi berbasis bukti

### 8.2 User Personas

#### Persona A: Ahli Gizi/Dietisien (Primary)
| Atribut | Detail |
|---------|--------|
| Usia | 23-40 tahun |
| Pekerjaan | Dietisien di RS/Klinik/Praktik Mandiri |
| Need | Database makanan lengkap, kalkulasi gizi cepat, manajemen pasien |
| Pain Point | Data gizi tersebar, kalkulasi manual memakan waktu |

#### Persona B: Mahasiswa Gizi (Secondary)
| Atribut | Detail |
|---------|--------|
| Usia | 18-24 tahun |
| Pekerjaan | Mahasiswa S1 Gizi/Profesi Dietisien |
| Need | Referensi data gizi untuk tugas/praktikum |
| Pain Point | Sulit akses TKPI, data tidak update |

#### Persona C: Pelaku Usaha Makanan (Tertiary)
| Atribut | Detail |
|---------|--------|
| Usia | 25-50 tahun |
| Pekerjaan | Pemilik UMKM/F&B, Food Consultant |
| Need | Komposisi gizi produk, info gizi untuk label |
| Pain Point | Tidak punya akses ke analisis lab, perlu data cepat |

### 8.3 Fitur Prioritas (MoSCoW)

#### Must Have (MVP)
- [x] ✅ Autentikasi (Email + Google OAuth)
- [x] ✅ CRUD Pasien
- [x] ✅ CRUD Intake (Rekam Asupan)
- [x] ✅ Kalkulator Gizi (Energi & Makronutrien)
- [x] ✅ Kalkulasi AKG
- [x] ✅ Database Makanan (Search, Filter, Pagination)
- [x] ✅ Profil AKG (Referensi Angka Kecukupan)
- [x] ✅ Manajemen Resep
- [x] ✅ Dashboard (Ringkasan Statistik)
- [x] ✅ i18n (Indonesia & Inggris)
- [x] ✅ Export/Hasil Perhitungan

#### Should Have
- [x] 🔄 Lock & Cancel Intake
- [x] 🔄 Snapshot Intake
- [x] 🔄 Feedback System
- [x] 🔄 Settings (Profile, Password, Contact)
- [ ] ⬜ Integrasi WebSocket (Realtime)
- [ ] ⬜ Grafik visual perbandingan gizi

#### Could Have
- [ ] 💡 Export PDF (Laporan Gizi)
- [ ] 💡 Import data batch (CSV/Excel)
- [ ] 💡 Dark Mode
- [ ] 💡 Mobile responsive enhancement
- [ ] 💡 API publik untuk developer

#### Won't Have (Saat Ini)
- [ ] ❌ AI/ML Recommendations
- [ ] ❌ Barcode Scanner
- [ ] ❌ Marketplace/Commerce
- [ ] ❌ Multi-tenant untuk institusi

### 8.4 Functional Requirements

| Fitur | ID | Deskripsi |
|-------|----|-----------|
| **Auth** | F-001 | Login dengan email & password |
| | F-002 | Login dengan Google OAuth |
| | F-003 | Register akun baru |
| | F-004 | Forgot & reset password |
| | F-005 | Update profil & password |
| **Dashboard** | F-006 | Lihat total pasien |
| | F-007 | Lihat total kalkulasi |
| **Pasien** | F-008 | Tambah pasien baru (nama, usia, BB, TB, gender) |
| | F-009 | Edit data pasien |
| | F-010 | Hapus pasien |
| | F-011 | Cari & filter daftar pasien |
| **Intake** | F-012 | Buat intake baru |
| | F-013 | Tambah makanan ke intake dengan porsi |
| | F-014 | Hapus makanan dari intake |
| | F-015 | Lock intake (finalisasi) |
| | F-016 | Cancel intake |
| | F-017 | Simpan snapshot hasil perhitungan |
| **Kalkulator** | F-018 | Hitung total energi & nutrisi |
| | F-019 | Hitung AKG berdasarkan profil |
| | F-020 | Tampilkan perbandingan asupan vs target |
| **Database Makanan** | F-021 | Browse semua makanan |
| | F-022 | Search makanan |
| | F-023 | Filter berdasarkan kategori |
| | F-024 | Tambah makanan baru |
| **Resep** | F-025 | Buat resep |
| | F-026 | Tambah makanan ke resep |
| | F-027 | Edit resep |
| | F-028 | Hapus resep |
| **AKG** | F-029 | Lihat daftar profil AKG |
| | F-030 | Filter AKG berdasarkan umur & gender |
| **Feedback** | F-031 | Kirim feedback |
| **Settings** | F-032 | Update profile information |
| | F-033 | Change password |
| | F-034 | Update contact number |

### 8.5 Non-Functional Requirements

| Aspek | Requirement |
|-------|-------------|
| **Performance** | Page load < 3 detik, API response < 500ms |
| **Security** | CSRF protection (Sanctum), HTTPS, XSS prevention |
| **Scalability** | Mendukung 1000+ user concurrent |
| **Reliability** | Uptime 99.9%, backup database harian |
| **Usability** | Mobile-responsive, aksesibilitas WCAG 2.0 |
| **Maintainability** | Modular code, dokumentasi API lengkap |
| **Data Integrity** | Validasi input, constraint database, referential integrity |

### 8.6 Metric & KPI

| Metrik | Target |
|--------|--------|
| Daily Active Users (DAU) | 500+ |
| Jumlah Pasien tercatat | 10.000+ |
| Jumlah Intake/kalkulasi per hari | 1.000+ |
| Database Makanan | 5.000+ entri |
| User Satisfaction Score | 4.5/5 |
| API Response Time | < 200ms average |
| Page Load Time | < 2 detik |

---

## 9. Rencana Rebuild

### 9.1 Rekomendasi Tech Stack untuk Rebuild

| Layer | Current | Recommended Rebuild | Alasan |
|-------|---------|-------------------|--------|
| **Frontend** | Nuxt 3 + Vue 3 | **Next.js 14+** atau **Nuxt 3 (stay)** | Nuxt 3 sudah baik, Next.js untuk ekosistem lebih luas |
| **UI** | Element Plus | **shadcn/ui** atau **Headless UI + Tailwind** | Lebih modern, performa lebih baik, kustomisasi tinggi |
| **Backend** | Laravel | **Laravel 11+ (stay)** atau **Go/Gin** | Laravel matang untuk API; Go untuk performa lebih tinggi |
| **Database** | MySQL/PostgreSQL | **PostgreSQL + TimescaleDB** | TimescaleDB untuk time-series intake data |
| **Cache** | Redis | **Redis (stay)** + **Meilisearch** | Meilisearch untuk full-text search makanan |
| **Auth** | Laravel Sanctum | **Laravel Sanctum (stay)** atau **Supabase Auth** | Sanctum sudah baik |
| **Realtime** | Laravel Reverb | **Laravel Reverb (stay)** atau **Pusher** | Reverb sudah native Laravel |
| **ORM** | Eloquent | **Prisma (jika pindah dari Laravel)** | Type-safe queries |
| **API Docs** | Scramble | **Scramble (stay)** atau **OpenAPI/Swagger** | Scramble auto-generate |
| **Storage** | Local | **S3-compatible (MinIO/DigitalOcean Spaces)** | Scalable, backup otomatis |
| **CI/CD** | - | **GitHub Actions + Docker** | Standard DevOps |
| **Monitoring** | - | **Sentry + Laravel Telescope** | Error tracking & debugging |
| **Testing** | - | **Pest PHP (backend) + Playwright (frontend)** | Comprehensive testing |

### 9.2 Arsitektur Rekomendasi

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Nuxt 3/Next.js)                    │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Pages/Components                                             │   │
│  │  ├── Tailwind CSS + shadcn/ui Components                     │   │
│  │  ├── Pinia/Zustand State Management                          │   │
│  │  ├── React Query/TanStack Query (caching & state)            │   │
│  │  └── Turbopack/Vite (HMR)                                     │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     API GATEWAY (Laravel/Golang)                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Services                                                     │   │
│  │  ├── Auth Service (Sanctum/JWT)                              │   │
│  │  ├── Patient Service                                         │   │
│  │  ├── Nutrition Calculator Service                            │   │
│  │  ├── AKG Calculation Engine                                  │   │
│  │  ├── Recipe Service                                          │   │
│  │  └── Search Service (Meilisearch)                            │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                       │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────────────┐  │
│  │  PostgreSQL    │  │    Redis       │  │   Meilisearch        │  │
│  │  (Primary DB)  │  │  (Session/     │  │  (Full-Text Search   │  │
│  │                │  │   Cache/Queue) │  │   Makanan)           │  │
│  └────────────────┘  └────────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE (Docker + VPS/Cloud)               │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Deployment                                                   │   │
│  │  ├── Docker Compose / Kubernetes                             │   │
│  │  ├── GitHub Actions CI/CD                                    │   │
│  │  ├── Nginx/Traefik Reverse Proxy                             │   │
│  │  └── Cloudflare CDN + SSL                                    │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 9.3 Timeline Rebuild (8-12 Minggu)

#### Fase 1: Foundation (Minggu 1-2)
```
Week 1-2:
├── Setup repository, Docker environment
├── Inisialisasi Laravel 11 + Nuxt 3
├── Setup database schema & migrations
├── Setup Meilisearch untuk search
├── Authentication system (Sanctum)
└── CI/CD pipeline (GitHub Actions)
```

#### Fase 2: Core MVP (Minggu 3-5)
```
Week 3-5:
├── Dashboard page
├── CRUD Pasien (full)
├── CRUD Intake (full)
├── Database Makanan (list, search, filter)
├── Kalkulator Gizi (inti engine)
├── AKG Calculator
└── Integration testing
```

#### Fase 3: Advanced Features (Minggu 6-7)
```
Week 6-7:
├── Manajemen Resep (CRUD + food mapping)
├── Profil AKG (browse, filter)
├── Lock/Cancel/Snapshot Intake
├── Settings (profile, password, contact)
├── Feedback system
└── i18n (Indonesia + Inggris)
```

#### Fase 4: Polish & Deployment (Minggu 8)
```
Week 8:
├── UI/UX polish (Tailwind + shadcn)
├── Responsive design
├── Performance optimization
├── Database indexing
├── Load testing
├── Documentation (README, API docs)
└── Production deployment
```

### 9.4 Database Migration Plan

```sql
-- Migration Plan (PostgreSQL)

-- 1. Users (enhanced)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    google_id VARCHAR(255) UNIQUE,
    role ENUM('admin', 'nutritionist', 'student') DEFAULT 'nutritionist',
    profile_photo_url TEXT,
    phone VARCHAR(20),
    email_verified_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. Foods (with full-text search)
CREATE TABLE foods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    name_fts TSVECTOR GENERATED ALWAYS AS (to_tsvector('indonesian', name)) STORED,
    category_id UUID REFERENCES food_categories(id),
    brand VARCHAR(255),
    serving_size DECIMAL(10,2) NOT NULL DEFAULT 100,
    serving_unit VARCHAR(50) DEFAULT 'gram',
    energy_kcal DECIMAL(10,2),
    protein_g DECIMAL(10,2),
    fat_g DECIMAL(10,2),
    carbohydrate_g DECIMAL(10,2),
    fiber_g DECIMAL(10,2),
    water_g DECIMAL(10,2),
    ash_g DECIMAL(10,2),
    -- 15+ additional nutrients
    vitamin_a_mcg DECIMAL(10,2),
    vitamin_c_mg DECIMAL(10,2),
    calcium_mg DECIMAL(10,2),
    phosphorus_mg DECIMAL(10,2),
    iron_mg DECIMAL(10,2),
    sodium_mg DECIMAL(10,2),
    potassium_mg DECIMAL(10,2),
    copper_mcg DECIMAL(10,2),
    zinc_mg DECIMAL(10,2),
    -- Metadata
    source ENUM('tkpi', 'manual', 'rumah_sakit', 'usda', 'brand', 'research'),
    verification_status ENUM('draft', 'verified', 'need_review') DEFAULT 'draft',
    verified_by UUID REFERENCES users(id),
    created_by UUID REFERENCES users(id) NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_foods_fts ON foods USING GIN(name_fts);

-- 3. Intakes (time-series optimized)
CREATE TABLE intakes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) NOT NULL,
    intake_date DATE NOT NULL DEFAULT CURRENT_DATE,
    meal_type VARCHAR(50), -- breakfast, lunch, dinner, snack
    status ENUM('active', 'locked', 'cancelled') DEFAULT 'active',
    notes TEXT,
    total_energy_kcal DECIMAL(10,2) GENERATED ALWAYS AS (...),
    -- calculated totals
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 4. Intake Details
CREATE TABLE intake_details (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    intake_id UUID REFERENCES intakes(id) ON DELETE CASCADE,
    food_id UUID REFERENCES foods(id),
    portion_size DECIMAL(10,2) NOT NULL,
    portion_unit VARCHAR(50) DEFAULT 'gram',
    calculated_energy DECIMAL(10,2),
    calculated_protein DECIMAL(10,2),
    -- all calculated nutrients
    created_at TIMESTAMP DEFAULT NOW()
);

-- 5. AKG Profiles
CREATE TABLE akg_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    age_group_id UUID REFERENCES age_groups(id),
    gender ENUM('male', 'female', 'all'),
    maternal_status ENUM('none', 'pregnant', 'breastfeeding'),
    -- Targets
    energy_kcal DECIMAL(10,2),
    protein_g DECIMAL(10,2),
    fat_g DECIMAL(10,2),
    carbohydrate_g DECIMAL(10,2),
    fiber_g DECIMAL(10,2),
    water_ml DECIMAL(10,2),
    -- All AKG targets
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 9.5 Key Improvements for Rebuild

| Aspek | Current | Improvement |
|-------|---------|-------------|
| **Search** | Basic LIKE query | Full-text dengan Meilisearch + autocomplete |
| **DB Indexing** | Minimal | Composite indexes + GIN for full-text |
| **Caching** | Not optimized | Redis cache layer + query caching |
| **API Response** | No pagination standard | Pagination + cursor-based for large datasets |
| **Error Handling** | Basic | Sentry + structured error responses |
| **Testing** | Minimal | Pest PHP (90% coverage target) |
| **CI/CD** | None | Automated testing + deployment |
| **Mobile** | Responsive web | Progressive Web App (PWA) + push notifications |
| **Data Validation** | Client-side only | Server-side validation + database constraints |
| **Audit Trail** | None | Activity logging for all CRUD operations |
| **Export** | None | PDF, Excel export untuk laporan |

### 9.6 Risiko & Mitigasi

| Risiko | Dampak | Mitigasi |
|--------|--------|----------|
| **Data Migration** | Kehilangan data historis | Backup penuh, migration script teruji, dry-run |
| **API Breaking Changes** | Frontend tidak kompatibel | Versioning API (/v1/), deprecation notice |
| **Database Performance** | Slow query untuk search besar | Indexing, Meilisearch, pagination |
| **User Adoption** | User tidak mau migrasi | Co-existence period, data export/import |
| **Keakuratan Data Gizi** | Klaim legal dari data salah | Validasi ahli gizi, disclaimer, referensi sumber |

---

## Lampiran

### A. Daftar Teknologi Detail

| Kategori | Saat Ini | Rekomendasi |
|----------|----------|-------------|
| **Runtime** | Node.js 18+ | Node.js 20+ (LTS) |
| **Package Manager** | npm/pnpm | pnpm |
| **Linter** | - | ESLint + Prettier |
| **Type Checking** | - | TypeScript (strict mode) |
| **Form Validation** | Element Plus native | Zod + react-hook-form / vee-validate |
| **Charts** | - | Chart.js / Recharts |
| **Date Handling** | - | dayjs / date-fns |
| **HTTP Client** | $fetch (Nuxt) | axios / $fetch + interceptors |

### B. Environment Variables

```env
# Frontend (.env)
NUXT_PUBLIC_API_URL=https://api-nutribase.nutrisee.id
NUXT_PUBLIC_GOOGLE_REDIRECT_URL=https://api-nutribase.nutrisee.id/oauth/google/redirect
NUXT_PUBLIC_REVERB_APP_KEY=bnV0cmliYXNl
NUXT_PUBLIC_REVERB_HOST=ws-nutribase.nutrisee.id
NUXT_PUBLIC_REVERB_PORT=443
NUXT_PUBLIC_REVERB_SCHEME=https
NUXT_PUBLIC_APP_TITLE=Nutribase

# Backend (.env)
APP_URL=https://nutribase.nutrisee.id
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=nutribase
DB_USERNAME=root
DB_PASSWORD=

SANCTUM_STATEFUL_DOMAINS=nutribase.nutrisee.id
SESSION_DOMAIN=.nutrisee.id

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

REVERB_APP_ID=
REVERB_APP_KEY=bnV0cmliYXNl
REVERB_APP_SECRET=
```

---

## 10. ML Feature Deep Dive: Meal Recommendation System

### 10.1 Overview

Sistem rekomendasi menu yang memberikan saran makanan/resep secara personal ke user berdasarkan:
- **Target gizi** (energi, protein, lemak, KH sesuai AKG pasien)
- **Riwayat intake** (makanan yang sering dikonsumsi)
- **Preferensi** (pantangan, alergi, preferensi diet)
- **Konteks** (waktu makan: pagi/siang/malam, jenis diet)

### 10.2 Data yang Dibutuhkan

#### Dari Database Existing Nutribase:

```sql
-- 1. Historical Intake Data (core)
CREATE TABLE recommendation_events (
    patient_id UUID,
    food_id UUID,
    recipe_id UUID NULL,
    intake_date TIMESTAMP,
    meal_type VARCHAR(20),        -- breakfast/lunch/dinner/snack
    portion_size DECIMAL(10,2),
    total_energy_kcal DECIMAL(10,2),
    total_protein_g DECIMAL(10,2),
    total_fat_g DECIMAL(10,2),
    total_carb_g DECIMAL(10,2),
    day_of_week INT,              -- 0=Monday..6=Sunday
    is_weekend BOOLEAN
);

-- 2. Patient Profile Features
CREATE TABLE patient_features (
    patient_id UUID PRIMARY KEY,
    age_group_id UUID,
    gender ENUM('male','female'),
    maternal_status VARCHAR(20),
    bmi DECIMAL(5,2),
    activity_level VARCHAR(20),
    dietary_preferences JSONB,    -- ["vegetarian","low_carb","diabetes"]
    food_allergies JSONB,         -- ["seafood","peanuts","gluten"]
    medical_conditions JSONB       -- ["diabetes","hypertension","ckd"]
);

-- 3. Food Nutritional Profile (Content Features)
CREATE TABLE food_nutrition_features (
    food_id UUID PRIMARY KEY,
    energy_density DECIMAL(10,2),  -- kcal/100g
    protein_ratio DECIMAL(5,4),    -- protein_kcal / total_kcal
    fat_ratio DECIMAL(5,4),
    carb_ratio DECIMAL(5,4),
    fiber_ratio DECIMAL(5,4),
    vitamin_score DECIMAL(5,2),
    mineral_score DECIMAL(5,2),
    category_embedding VECTOR(64), -- categorical encoding
    ingredient_tags TEXT[]          -- ["rice","chicken","vegetable"]
);
```

### 10.3 Arsitektur ML

```
┌──────────────────────────────────────────────────────────────────────┐
│                        SISTEM REKOMENDASI                             │
│                                                                      │
│  ┌─────────────────────────┐    ┌────────────────────────────────┐   │
│  │   CONTENT-BASED         │    │   COLLABORATIVE FILTERING     │   │
│  │   FILTERING (CBF)       │    │   (CF)                        │   │
│  │                         │    │                                │   │
│  │  "Rekomendasi mirip     │    │  "Pasien mirip makan apa?"    │   │
│  │   dengan yang disukai"  │    │                                │   │
│  └───────────┬─────────────┘    └──────────────┬─────────────────┘   │
│              │                                 │                      │
│              ▼                                 ▼                      │
│  ┌─────────────────────────┐    ┌────────────────────────────────┐   │
│  │  Food Nutritional       │    │  Patient-Food Interaction     │   │
│  │  Similarity (cosine)    │    │  Matrix Factorization (SVD)   │   │
│  │  Ingredient Similarity  │    │  KNN Patient Neighborhood     │   │
│  └───────────┬─────────────┘    └──────────────┬─────────────────┘   │
│              │                                 │                      │
│              └──────────────┬──────────────────┘                      │
│                             ▼                                        │
│              ┌─────────────────────────────┐                         │
│              │   HYBRID ENSEMBLE            │                        │
│              │   Weighted Combination       │                        │
│              │   + Rule-based Constraints   │                        │
│              │   (alergi, diet, penyakit)   │                        │
│              └─────────────┬───────────────┘                         │
│                            ▼                                         │
│              ┌─────────────────────────────┐                         │
│              │   FINAL RECOMMENDATION       │                        │
│              │   5-10 makanan/resep         │                        │
│              │   + rationale (kenapa)       │                        │
│              └─────────────────────────────┘                         │
└──────────────────────────────────────────────────────────────────────┘

    INFRA:
    ┌──────────────────────────────────────────────────────────────────┐
    │  Python FastAPI (microservice)                                   │
    │  ├── scikit-learn (KNN, SVD, TF-IDF)                            │
    │  ├── pandas + numpy (feature engineering)                       │
    │  ├── PostgreSQL pgvector (vector similarity)                    │
    │  └── Redis Cache (precompute rekomendasi harian)                │
    └──────────────────────────────────────────────────────────────────┘
```

### 10.4 Algoritma Detail

#### A. Content-Based Filtering (CBF)

**Cara Kerja:**
1. Setiap makanan direpresentasikan sebagai vector fitur nutrisi
2. Hitung similarity cosine antara makanan yang pernah dikonsumsi vs semua makanan
3. Rekomendasikan makanan dengan similarity tertinggi

```python
# Pseudocode implementasi
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ContentBasedRecommender:
    def __init__(self):
        self.scaler = StandardScaler()
        self.food_vectors = None  # Matrix: [n_foods x n_features]
        self.food_ids = []

    def build_food_profiles(self, foods_df):
        """
        Feature vector tiap makanan:
        - energy_kcal, protein_g, fat_g, carbohydrate_g (standardized)
        - protein_ratio, fat_ratio, carb_ratio
        - fiber_density, vitamin_score, mineral_score
        - category_onehot (dummy encoding)
        """
        feature_cols = [
            'energy_kcal', 'protein_g', 'fat_g', 'carbohydrate_g',
            'fiber_g', 'protein_ratio', 'fat_ratio', 'carb_ratio',
        ] + [col for col in foods_df.columns if col.startswith('cat_')]

        self.food_ids = foods_df['id'].tolist()
        self.food_vectors = self.scaler.fit_transform(foods_df[feature_cols])

    def recommend(self, patient_history_ids, top_n=10):
        """
        Ambil rata-rata vector makanan yang pernah dikonsumsi pasien,
        lalu cari makanan paling mirip (cosine similarity).
        """
        history_idx = [self.food_ids.index(fid)
                       for fid in patient_history_ids
                       if fid in self.food_ids]

        if not history_idx:
            return self._popular_fallback()

        profile_vector = np.mean([self.food_vectors[i]
                                  for i in history_idx], axis=0)

        similarities = cosine_similarity(
            profile_vector.reshape(1, -1),
            self.food_vectors
        )[0]

        # Exclude already consumed
        similarities[history_idx] = -1

        top_indices = np.argsort(similarities)[-top_n:][::-1]
        return [self.food_ids[i] for i in top_indices]

    def _popular_fallback(self):
        """Cold-start: return makanan paling populer"""
        pass
```

#### B. Collaborative Filtering (CF)

**Cara Kerja:**
- **User-based CF**: Cari pasien dengan pola intake mirip, rekomendasikan makanan mereka
- **Item-based CF**: Makanan yang sering dimakan bersamaan, rekomendasikan pasangan

```python
# Matrix Factorization dengan SVD
from sklearn.decomposition import TruncatedSVD

class CollaborativeRecommender:
    def __init__(self, n_factors=20):
        self.n_factors = n_factors
        self.svd = TruncatedSVD(n_components=n_factors)
        self.patient_food_matrix = None
        self.patient_ids = []
        self.food_ids = []

    def build_interaction_matrix(self, intakes_df):
        """
        Matrix: [n_patients x n_foods]
        Value: frequency of consumption (normalized)
        Atau: rating implisit (1 jika pernah dikonsumsi)
        """
        self.patient_food_matrix = intakes_df.pivot_table(
            index='patient_id',
            columns='food_id',
            values='frequency',
            fill_value=0
        )
        self.patient_ids = self.patient_food_matrix.index.tolist()
        self.food_ids = self.patient_food_matrix.columns.tolist()

    def train(self):
        """Faktorisasi matrix untuk latent features"""
        matrix = self.patient_food_matrix.values
        self.fitted_svd = self.svd.fit(matrix)

    def recommend(self, patient_id, top_n=10):
        """Rekomendasi makanan yang belum pernah dikonsumsi"""
        patient_idx = self.patient_ids.index(patient_id)
        patient_vector = self.patient_food_matrix.iloc[patient_idx].values.reshape(1, -1)

        # Prediksi rating untuk semua makanan
        predicted = self.fitted_svd.inverse_transform(
            self.fitted_svd.transform(patient_vector)
        )[0]

        # Exclude already consumed
        predicted[patient_vector[0] > 0] = -1

        top_indices = np.argsort(predicted)[-top_n:][::-1]
        return [self.food_ids[i] for i in top_indices]
```

#### C. Hybrid (CBF + CF + Rule-based)

```python
class HybridMealRecommender:
    def __init__(self):
        self.cbf = ContentBasedRecommender()
        self.cf = CollaborativeRecommender()
        self.weights = {'cbf': 0.4, 'cf': 0.4, 'rules': 0.2}

    def recommend(self, patient, context, top_n=5):
        """
        patient: {id, age_group, gender, bmi, allergies, conditions, preferences}
        context: {meal_type, target_energy, target_protein, etc}
        """

        # 1. Dapatkan candidate dari CBF + CF
        cbf_candidates = self.cbf.recommend(patient['history_ids'], top_n=20)
        cf_candidates = self.cf.recommend(patient['id'], top_n=20)

        candidates = set(cbf_candidates) | set(cf_candidates)

        # 2. Score tiap candidate
        scored = []
        for food_id in candidates:
            score = 0

            # CBF score
            if food_id in cbf_candidates:
                score += self.weights['cbf'] * cbf_candidates.index(food_id)

            # CF score
            if food_id in cf_candidates:
                score += self.weights['cf'] * cf_candidates.index(food_id)

            # Rule-based: constraint satisfaction
            rule_score = self._evaluate_constraints(
                food_id, patient, context
            )
            score += self.weights['rules'] * rule_score

            scored.append((food_id, score))

        # 3. Sort & return top N
        scored.sort(key=lambda x: -x[1])
        return scored[:top_n]

    def _evaluate_constraints(self, food_id, patient, context):
        """
        Rule-based scoring:
        - Apakah sesuai target energi? (+)
        - Apakah cocok untuk diabetes? (+/-)
        - Apakah mengandung alergen? (-10)
        - Apakah sesuai preferensi diet? (+)
        - Apakah sesuai meal_type (sarapan vs dinner)? (+)
        """
        score = 0
        food = self._get_food(food_id)

        # Target energy match (dalam 20% dari target)
        if context['target_energy']:
            diff = abs(food['energy_kcal'] - context['target_energy'])
            if diff / context['target_energy'] <= 0.2:
                score += 3

        # Alergi check (hard constraint)
        if patient.get('allergies'):
            if any(a in (food.get('allergens') or []) for a in patient['allergies']):
                score -= 10  # Eliminate

        # Preferensi diet
        if patient.get('preferences'):
            if any(p in (food.get('diet_tags') or []) for p in patient['preferences']):
                score += 2

        return max(score, 0)
```

### 10.5 Dataset yang Dibutuhkan untuk Training

| Dataset | Sumber | Jumlah Data Minimal | Format |
|---------|--------|-------------------|--------|
| **Patient-Food Interactions** | Tabel `intakes` + `intake_details` | 10.000+ records | `{patient_id, food_id, frequency, meal_type, timestamp}` |
| **Food Nutritional Profiles** | Tabel `foods` | 1.000+ foods | `{food_id, energy, protein, fat, carb, fiber, category}` |
| **Patient Profiles** | Tabel `patients` | 500+ patients | `{age, gender, bmi, kondisi, preferensi}` |
| **Recipe Compositions** | Tabel `recipe_foods` | 200+ recipes | `{recipe_id, food_id, amount}` |
| **Feedback eksplisit** | Tabel `feedbacks` | 100+ | `{user_id, food_id, rating (liked/disliked)}` |

### 10.6 Pipeline ML End-to-End

```
Batch Training (Harian/Mingguan):
┌──────────┐   ┌───────────┐   ┌──────────┐   ┌───────────┐
│ Extract  │──►│ Transform │──►│ Train    │──►│ Save      │
│ Data     │   │ Feature   │   │ Model    │   │ Model     │
│ (SQL)    │   │ Eng       │   │ (SVD)    │   │ (.pkl)    │
└──────────┘   └───────────┘   └──────────┘   └───────────┘
                                                     │
Real-time Inference:                                  ▼
┌──────────┐   ┌───────────┐   ┌──────────┐   ┌───────────┐
│ Request  │──►│ Load      │──►│ Predict  │──►│ Return    │
│ /recommend│  │ Model     │   │ Score    │   │ Top 5-10  │
│ patient=X│   │ + Rules   │   │ + Filter │   │ Meals     │
└──────────┘   └───────────┘   └──────────┘   └───────────┘
```

### 10.7 API Design

```json
POST /api/ml/recommend/meals
{
    "patient_id": "uuid",
    "context": {
        "meal_type": "breakfast",
        "target_energy_kcal": 450,
        "target_protein_g": 20,
        "dietary_preferences": ["low_carb"],
        "exclude_foods": ["uuid1", "uuid2"],
        "max_results": 5
    }
}

Response:
{
    "recommendations": [
        {
            "food_id": "uuid",
            "name": "Telur Dadar + Sayur",
            "reason": "Rendah karbohidrat, tinggi protein (cocok untuk diet Anda)",
            "nutrition": {
                "energy_kcal": 380,
                "protein_g": 22,
                "fat_g": 18,
                "carbohydrate_g": 8
            },
            "match_score": 0.92,
            "source": "hybrid"
        }
    ],
    "meta": {
        "model_version": "v2.3",
        "inference_time_ms": 45,
        "explanation": "Rekomendasi berdasarkan preferensi low-carb + riwayat sarapan + constraint diabetes"
    }
}
```

### 10.8 Cold Start Strategy

| Situasi | Strategy |
|---------|----------|
| **Pasien baru** (no history) | Rekomendasi berdasarkan rules: umur + gender + BMI → target AKG → cocokkan makanan |
| **Makanan baru** (no interactions) | Content-based only (similarity nutrisi ke makanan existing) |
| **User baru + food baru** | Fallback: most popular by meal_type + category |
| **Data intake sedikit** | Weight CBF > CF, tambah exploration (random sampling) |

### 10.9 Evaluation Metrics

| Metric | Target | Cara Ukur |
|--------|--------|-----------|
| **Precision@k** | > 0.6 | Dari total rekomendasi, berapa yang dipilih user |
| **Recall@k** | > 0.4 | Dari total makanan dikonsumsi, berapa yang terekomendasi |
| **NDCG@k** | > 0.7 | Ranking quality (apakah top rekomendasi yang paling relevan) |
| **Coverage** | > 80% | Berapa banyak makanan dalam DB yang pernah direkomendasikan |
| **Serendipity** | > 0.3 | Apakah rekomendasi mengejutkan tapi relevan? |
| **A/B Test CTR** | +15% | Click-through rate dibanding tanpa rekomendasi |

### 10.10 Implementation Timeline (6-8 Minggu)

| Phase | Task | Duration |
|-------|------|----------|
| **Phase 1** | Setup ML infra (FastAPI, pgvector, Redis) | 1 minggu |
| **Phase 2** | ETL pipeline: extract intake data → feature matrix | 1 minggu |
| **Phase 3** | Implement CBF + CF + Hybrid models | 2 minggu |
| **Phase 4** | Rule engine: alergi, diet, penyakit, target gizi | 1 minggu |
| **Phase 5** | API integration + frontend UI (rekomendasi card) | 1 minggu |
| **Phase 6** | Testing, evaluation, A/B test | 1 minggu |
| **Phase 7** | Deploy, monitoring, iteration | 1 minggu |

### 10.11 Contoh Sederhana (Step-by-Step)

```
INPUT: Pasien = "Budi", laki-laki, 35th, BB=75, TB=170
       Target: Sarapan (~400 kkal, protein 20g, rendah karbo)
       Riwayat: suka telur, ayam, brokoli
       Alergi: seafood
       Preferensi: low-carb, diabetes

STEP 1: Cari profil nutrisi makanan yang Budi suka
STEP 2: CBF → cari makanan dengan profil nutrisi mirip
         (telur → daging ayam, tahu, tempe)
STEP 3: CF → cari pasien mirip (30-40th, pria, diabetes) → mereka makan apa?
         (oatmeal, telur rebus, sayur tumis)
STEP 4: Filter:
         ✅ Telur Rebus (80kkal) → ✓ protein tinggi, 0 karbo
         ✅ Omelet Sayur (250kkal) → ✓ cocok sarapan
         ✅ Tumis Brokoli + Tahu (150kkal) → ✓ sayur favorit
         ❌ Udang Goreng → ✗ alergi seafood
         ❌ Nasi Uduk → ✗ tinggi karbo, tidak cocok diabetes
STEP 5: Rank + return Top 3:
         1. Omelet Sayur (skor: 0.92)
         2. Telur Rebus + Tumis Brokoli (skor: 0.88)
         3. Tahu Bacem + Sayur (skor: 0.75)
```

### 10.12 Keuntungan untuk Nutribase

| Aspek | Tanpa ML | Dengan ML |
|-------|----------|-----------|
| **Input intake** | Manual cari satu-satu | Auto-rekomendasi dari yang sering dipakai |
| **Perencanaan menu** | Tidak ada | Generate menu harian sesuai target AKG |
| **Edukasi pasien** | Manual | Rekomendasi + alasan nutrisi (edukatif) |
| **Efisiensi ahli gizi** | 15-20 menit per pasien | 5-10 menit per pasien |
| **Personalization** | Semua pasien sama | Per individu berdasarkan profil + riwayat |

---

*Dokumen ini dibuat berdasarkan hasil reverse engineering menyeluruh terhadap aplikasi Nutribase by Nutrisee pada tanggal 9 Juli 2026. Seluruh informasi dikumpulkan dari analisis kode frontend (JavaScript bundle), endpoint API, konfigurasi publik, dan sumber terbuka.*
