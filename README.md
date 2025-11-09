# 🪂 DropSpot – Limited Stock & Waitlist Platform

**Başlangıç zamanı:** `2025-11-08 00:05 (UTC+3)`
**Süre:** 72 saat
**Tamamlanma:** `2025-11-09`
**Seed:** `106de63e8906` *(otomatik hesaplanan özgün seed değeri)*

---

## 🎯 Amaç

DropSpot, sınırlı stokla yayımlanan özel ürün veya etkinliklerin yönetildiği, kullanıcıların bekleme listesine katılabildiği ve "claim window" açıldığında hak kazanabildiği bir platformdur.
Amaç, bu süreci **adil, ölçeklenebilir ve idempotent** hale getirmektir.

---

## 🧩 Mimari Genel Bakış

```
.
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── drops.py
│   │   │   └── admin.py
│   │   ├── db.py
│   │   └── config.py
│   ├── alembic/
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx
│   │   │   ├── signup/page.tsx
│   │   │   ├── drops/[id]/page.tsx
│   │   │   └── admin/page.tsx
│   │   ├── lib/api.ts
│   │   └── __tests__/
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
└── .github/workflows/ci.yml
```

**Teknolojiler:**

* **Backend:** FastAPI + SQLAlchemy + Alembic + PostgreSQL
* **Frontend:** Next.js (React + TypeScript + Tailwind)
* **CI/CD:** GitHub Actions
* **Container:** Docker Compose

---

## 🧠 Veri Modeli

### Tablo: `users`

| Alan            | Tip    | Açıklama                    |
| --------------- | ------ | --------------------------- |
| id              | UUID   | Benzersiz kullanıcı kimliği |
| email           | String | Kullanıcı e-posta adresi    |
| hashed_password | String | Şifre hash değeri           |

### Tablo: `drops`

| Alan               | Tip      | Açıklama                   |
| ------------------ | -------- | -------------------------- |
| id                 | UUID     | Drop kimliği               |
| title              | String   | Ürün/etkinlik adı          |
| description        | Text     | Açıklama                   |
| stock              | Integer  | Toplam stok                |
| claim_window_start | Datetime | Hak talep başlangıç zamanı |
| claim_window_end   | Datetime | Hak talep bitiş zamanı     |

### Tablo: `waitlist`

| user_id | drop_id | joined_at |

### Tablo: `claims`

| user_id | drop_id | claim_code |

---

## 🚀 API Endpoint’leri

| Method   | Endpoint            | Açıklama                           |
| -------- | ------------------- | ---------------------------------- |
| `POST`   | `/auth/signup`      | Kullanıcı kaydı                    |
| `GET`    | `/drops`            | Aktif drop listesi                 |
| `POST`   | `/drops/{id}/join`  | Bekleme listesine katıl            |
| `POST`   | `/drops/{id}/leave` | Bekleme listesinden ayrıl          |
| `POST`   | `/drops/{id}/claim` | Hak talep et (claim window içinde) |
| `POST`   | `/admin/drops`      | Yeni drop oluştur (Admin)          |
| `PUT`    | `/admin/drops/{id}` | Drop güncelle                      |
| `DELETE` | `/admin/drops/{id}` | Drop sil                           |

Tüm `/admin` uçları `X-Admin-Key` header‑ı gerektirir.

---

## 🔁 Idempotency & Transaction Mantığı

* Waitlist ve claim işlemleri **unique constraint** + **transaction** ile garanti altına alınmıştır.
* Aynı kullanıcı aynı işlemi tekrar denediğinde sonuç değişmez.
* Backend `SQLAlchemy` transaction’larını ve PostgreSQL `ON CONFLICT DO NOTHING` mekanizmasını kullanır.

---

## 🧮 Seed ve Priority Score

**Seed üretimi:**

```bash
remote=$(git config --get remote.origin.url)
epoch=$(git log --reverse --format=%ct | head -n1)
start="202511080005"
raw="$remote|$epoch|$start"
seed=$(python3 -c "import hashlib; print(hashlib.sha256('$raw'.encode()).hexdigest()[:12])")
```

**Kullanım:**

```python
A = 7 + (int(seed[0:2],16) % 5)
B = 13 + (int(seed[2:4],16) % 7)
C = 3 + (int(seed[4:6],16) % 3)

priority_score = base + (signup_latency_ms % A) + (account_age_days % B) - (rapid_actions % C)
```

Bu skor sistemi kullanıcı önceliğini belirler.

---

## 🧪 Testler

### Backend

* **Unit Test:** `test_seed.py` – priority_score deterministik test
* **Integration Test:** `test_drops.py` – waitlist & claim idempotency akışı
* **Admin CRUD Test:** `test_admin.py` – Admin create/update/delete doğrulaması

### Frontend

* **Component Test:** `home.test.tsx`, `admin.test.tsx`
* **E2E Smoke:** Drop listesi ve admin panel yükleniyor mu

---

## ⚙️ Kurulum

### Local Development

```bash
git clone <repo_url>
cd drop-spot-case
docker compose up --build
```

Frontend: [http://localhost:3000](http://localhost:3000)
Backend: [http://localhost:8000/docs](http://localhost:8000/docs)

### Alembic Migration (gerekirse)

```bash
docker compose exec backend alembic upgrade head
```

## ⚡ Teknik Tercihler ve Katkılar

* **FastAPI + SQLAlchemy** seçilme nedeni: basit async yapısı ve güçlü transaction yönetimi
* **Next.js + Tailwind**: sade, hızlı UI geliştirme süreci
* **Docker Compose**: tam izole, reproducible ortam
* **CI/CD (GitHub Actions)**: her commit sonrası test & build

---

## 🏁 Sonuç

DropSpot;

* Adil ve deterministik işlem yapısı,
* Güçlü test kapsamı,
* Anlamlı commit geçmişi ve CI entegrasyonu
  ile uçtan uca üretim kalitesinde bir örnek projedir.
