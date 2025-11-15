<<<<<<< HEAD
# 🚗 AI-Powered Vehicle Condition Assessment — Hiring Sprint

## 🧩 Overview

Build a working prototype for **AI-powered vehicle condition assessment**. The system should allow users to capture/upload vehicle images at pick-up and return, automatically detect damages, and display a report.

The solution can be a **web** or **mobile** app. Use of pretrained AI/ML models or APIs is allowed.

---

## 🎯 Goal / Business Requirements

**Business Goal:** Automate and simplify vehicle condition inspections for rental businesses (cars, scooters, boats, equipment). Enable customers and staff to:

- Capture/upload vehicle images at pick-up and return
- Detect and compare damages between pick-up and return
- Estimate severity and cost of damages
- Display results in a dashboard or report
- Integrate with 3rd party systems via API

**Example Workflow:**

1. Customer picks up a car, takes photos via the app.
2. On return, new photos are taken.
3. The system compares images, highlights new damages, and estimates repair costs.
4. A summary report is shown in the UI and available via API.

---

## 📦 Deliverables

- Deployed Service URL: Public link
- UI: Web or mobile interface for image upload, damage detection, and report display
- API: REST or GraphQL endpoint for 3rd party integration
- README: Setup and usage instructions
  
---

## 🏆 Selection Criteria

- Functionality & Stability: Does the project meet the core requirements? Are all main features working correctly without crashes or bugs?
- Code Quality & Structure: Clean, modular, readable code. Proper use of version control, comments, and naming conventions.
- Technical Implementation & Innovation: Appropriate choice of tech stack, API integrations, and efficient logic. AI integration.
- Business Alignment: Does the solution address Aspire’s business case ?
- UI/UX & Presentation: User interface quality, accessibility, and overall user experience.

---

## ☁️ Deployment Requirements

- For webapp, you are free to deploy anywhere: [Vercel](https://vercel.com/), [Netlify](https://www.netlify.com/), [Render](https://render.com/), [Google Cloud Run](https://cloud.google.com/run), [Hugging Face Spaces](https://huggingface.co/spaces), etc.
- For mobile apps, if cloud deployment is not possible, share the APK or Expo link

---

## 💎 Bonus Points

- Testing: Automated tests + instructions to run them
- Documentation: API docs (Swagger/OpenAPI/GraphQL)
- CI/CD: Pipeline for automated deployment
- Dockerfile

---

## 🛠️ Resources

### Deployment Free Resources

- [Vercel](https://vercel.com/) — Web frontend
- [Netlify](https://www.netlify.com/) — Web frontend
- [Render](https://render.com/) — Web or backend
- [Google Cloud Run](https://cloud.google.com/run) — Backend containers
- [Expo](https://expo.dev/) — React Native mobile apps

### AI Models / LLMS

- You are free to use any free/open-source models, libraries, or APIs.
- You may host your own solution or use a publicly available API, whatever works best for your prototype.
- The goal is a working, reproducible prototype. Accuracy and cleverness will be evaluated, but you don’t need a production-level solution.

---

## 📝 Pro Tips / Implementation Notes

- Focus first on business requirements and core functionality. A working prototype is better than a fancy but incomplete solution.
- You can store images however it makes sense (in memory, temp files, cloud storage, etc.)
- Show results clearly in the UI: side-by-side images, highlights, and summary reports.
- Prioritize clean, modular code and reproducibility for easy evaluation.
- You may combine multiple tools to detect, score, and summarize damages.

---

## 📬 Submission Guide

- Fork the repo to your own GitHub repository
- Commit changes regularly and push all code to your repo
- Deploy your solution to a cloud provider (make sure the URL is public)
- Submit your solution [here](https://tally.so/r/VLEkQv)
  
---


> 🏁 **Good luck!** Focus on a **working prototype**, clear UI, and AI-powered inspection summary 🚀.
=======
# Vehicle Damage Detection & Repair Cost Estimation

End‑to‑end prototype for uploading vehicle photos, detecting damages with a YOLO model, and returning an exact USD repair estimate. It supports single-image analysis and before/after comparison, exposes an API for integrations, and ships with a modern web UI.

## Tech Stack

- frontend/ — React + Vite (TypeScript)
- backend/  — Laravel API (proxies to ML, future: auth, storage, DB)
- ml/       — FastAPI service (loads YOLO once; cost rules in USD)

## Project Structure

```
.
├─ frontend/            # React app (upload UI, comparison, PDF reports)
├─ backend/             # Laravel API (predict/compare endpoints)
├─ ml/                  # Python ML microservice (YOLO + cost engine)
│  ├─ api.py            # FastAPI endpoints /predict, /compare
│  ├─ services/         # inference.py runtime detection and costing
│  ├─ assets/
│  │  ├─ cost_rules.json            # USD parts/labor/paint defaults
│  │  └─ car_damage_price.json      # legacy ranges (fallback)
│  ├─ model/
│  │  └─ best.pt       # YOLO weights (place your file here)
│  └─ requirements.txt
└─ .venv/               # optional Python virtualenv (local use)
```

## Prerequisites

- Node 18+ and npm
- PHP 8.2+ and Composer
- Python 3.9–3.11 (recommended) and pip

## Quickstart (3 terminals)

1) Start the ML service (port 8001)

```bash
cd ml
python -m venv ..\.venv  # if you don't have one yet
..\ .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt

# Optional: adjust cost parameters at runtime
set LABOR_RATE_USD=95
set PAINT_RATE_USD=120
set MATERIALS_USD=50

python -m uvicorn ml.api:app --reload --host 127.0.0.1 --port 8001
```

Notes:
- Make sure `ml/model/best.pt` exists (copy your YOLO weights here).
- You can customize `ml/assets/cost_rules.json` to tune exact USD estimates.
- We draw detection boxes with OpenCV (`opencv-python-headless` is in the requirements).
- Verify the API:
  ```bash
  curl -v http://127.0.0.1:8001/docs
  ```

2) Start the Laravel backend (port 8000)

```bash
cd backend
composer install
copy .env.example .env
notepad .env
```

In `.env`, add:

```
APP_URL=http://localhost:8000
FILESYSTEM_DISK=public
ML_BASE=http://127.0.0.1:8001
```

Then:

```bash
php artisan key:generate
php artisan migrate
php artisan storage:link
php artisan optimize:clear
php artisan serve --port=8000
```
You can verify routes with:
```bash
php artisan route:list
```

3) Start the React frontend

```bash
cd frontend
npm install
echo VITE_API_BASE=http://localhost:8000> .env
npm run dev
```

Open the URL shown (typically `http://localhost:5173`). Upload an image or use the **Before / After** tab. You’ll see the original and detected images side‑by‑side (boxes only), a per‑class summary, and an exact USD total. You can also download a simple PDF‑style report.

### Camera capture
- On Single and Compare tabs, click “Use Camera” to capture photos via `getUserMedia`. Works on `http://localhost` or any `https://` origin.

## API (ML service)

Run: `uvicorn ml.api:app --reload --port 8001`

- POST `/predict` — form field `image` (file)
  - Returns JSON with `classes`, `detections` (class, confidence, each_cost_usd), `counts`, `per_class_costs`, `totals`, and `annotated_image_b64` (PNG).
- POST `/compare` — form fields `before`, `after` (files)
  - Returns JSON with before/after counts, new-damage counts/costs, and annotated images as base64.

### Pricing modes
- Configure before starting the ML service:
  - `PRICE_PROVIDER=rule | ml | hybrid` (default `rule`)
  - `PRICE_BLEND_ALPHA=0.6` (only for `hybrid`: final = α·ML + (1–α)·rule)
  - `COST_MULTIPLIER=0.6` (global scaler for rule/area pricing)
  - Area scaling (rule path): `AREA_REF` (0.15), `AREA_MIN_SCALE` (0.25), `AREA_GAMMA` (0.7)

When `ml`/`hybrid` is enabled, `/predict` includes:
```json
{
  "totals_rule": { "min": 1234, "currency": "USD" },
  "price": { "provider": "ml", "ml_usd": 1190.5, "rule_usd": 1234, "final_usd": 1190.5 }
}
```

### Train ML price regressor (optional)
Create a CSV `ml/data/claims.csv` with:
```
image_path,vehicle_type,total_usd
C:\data\car\img001.jpg,car,1450
```
Train and save:
```bash
pip install -r ml/requirements.txt
python -m ml.train_price_gbm --csv ml/data/claims.csv --out ml/models/price_gbm.pkl
```
Run ML with `PRICE_PROVIDER=ml` (or `hybrid`).

### Swagger / OpenAPI
- FastAPI docs at `http://127.0.0.1:8001/docs` (Swagger UI) and `/redoc`.

## Backend API (Laravel)

- `POST /api/predict` — accepts `image` (file). Proxies to ML `/predict`, persists a “single” claim with original/annotated paths and totals, returns ML payload plus `claim_id`.
- `POST /api/compare` — accepts `before`, `after` (files). Proxies to ML `/compare`, persists a “compare” claim with before/after + annotated paths and totals, returns ML payload plus `claim_id`.
- `GET /api/claims` — paginated list of saved claims (supports `?type=single|compare`).
- `GET /api/claims/{id}` — single claim record.

## Cost Estimation

- Exact USD totals are computed via `ml/assets/cost_rules.json`:

```json
{
  "Minor":    { "parts_usd": 200,  "labor_h": 1.5,  "paint_h": 0.5 },
  "Moderate": { "parts_usd": 650,  "labor_h": 4.0,  "paint_h": 2.0 },
  "Severe":   { "parts_usd": 1800, "labor_h": 10.0, "paint_h": 4.0 }
}
```

- Runtime overrides (env): `LABOR_RATE_USD`, `PAINT_RATE_USD`, `MATERIALS_USD`.
- If rules are missing, the service falls back to a midpoint USD conversion from legacy ranges.

## Common Issues

- ML not reachable: ensure Terminal A is running `uvicorn` with `--host 127.0.0.1 --port 8001`; try `curl -v http://127.0.0.1:8001/docs`.
- 500 on `/api/predict` or `/api/compare`:
  - Run `php artisan migrate` and `php artisan storage:link` in `backend/`.
  - Ensure `ML_BASE=http://127.0.0.1:8001` and restart `php artisan serve`.
  - Inspect `backend/storage/logs/laravel.log` for details.
- 404 on `/api/predict`: verify routes with `php artisan route:list`.
- CORS issues: `backend/config/cors.php` allows `http://localhost:5173` by default.
- Large camera images: backend allows up to ~20 MB per image—reduce resolution if needed.

## Docker

`docker-compose.yml` provided. To run:
```bash
docker compose up --build
```
Services:
- ML (8001), Backend (8000), Frontend (5173)

## Roadmap

- Persist claims and results in Laravel (DB + S3)
- Admin dashboard and user roles
- Better PDF reports and email share
- Docker Compose for one-command local run

---

Questions or ideas? Open an issue or PR. Contributions are welcome!

>>>>>>> f0d99606f950aac794e470fe706a8fbf0dfe2e0e
