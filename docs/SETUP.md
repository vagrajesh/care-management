# Setup

## Prerequisites
- Python 3.14
- Node 24 (runs `.ts` files directly)
- PostgreSQL 18

## 1. Database
1. Create a database and an application user (example user: `fde_user`).
2. As the table owner, run [db/schema.sql](../db/schema.sql). Adjust the user name in the `GRANT` lines if yours differs.

The application user cannot `ALTER` tables it does not own. Schema changes must be run by the owner.

## 2. Environment
Copy `.env.example` to `.env` in the project root and set `DATABASE_URL`:

```
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/DBNAME
```

`.env` holds credentials. Never commit it.

## 3. Backend
```powershell
pip install -r backend/requirements.txt
cd backend\src
python -m uvicorn main:app --reload
```
API runs at `http://127.0.0.1:8000` and interactive docs at `/docs`.

## 4. Load data
Loads `data/Diabetic_data_Selected_column.csv`, cleans each row, calculates `risk_score` and `risk_level`, and inserts 101,766 rows:

```powershell
cd practice
python bulk_load.py
```

## 5. Frontend
```powershell
cd frontend
npm install
cd src
node fetchEncounters.ts
```
Scripts need the API running. `package.json` sets `"type": "module"`.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `GET /` returns 404 | Expected. There is no root route. Use `/docs` or an endpoint. |
| `InsufficientPrivilege` on `care_interventions` | Run the `GRANT` statements in `db/schema.sql` as the owner. |
| `DATABASE_URL is not set` | `.env` missing or not in the project root. |
| `Cannot find name 'process'` in the editor | Run `npm install` in `frontend` (installs `@types/node`). |
| Node fails with "Failed to load the ES module" | `"type": "module"` missing in `frontend/package.json`. |
