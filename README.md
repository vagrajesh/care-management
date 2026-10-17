# Care Management

Prototype that scores hospital encounters for readmission risk and gives a care team a prioritized queue to work.

## Tech stack

| Layer | Technology |
|---|---|
| Database | PostgreSQL 18 |
| Backend | Python 3.14, FastAPI 0.115, uvicorn 0.31, Pydantic 2.12, psycopg 3.3, python-dotenv |
| Frontend | TypeScript run directly by Node 24 (`node file.ts`), `@types/node` |
| Data | Diabetes 130-US hospitals dataset (`data/`), 101,766 encounters |

## Project structure

```
backend/src/   FastAPI app: main.py, service.py, repository.py, model.py, database_conn.py
backend/requirements.txt
frontend/src/  types/ (interfaces) and fetch*.ts scripts
db/schema.sql  Table definitions and grants
docs/API.md    Endpoint specs (source of truth)
docs/SETUP.md  Installation and database setup
practice/      Practice scripts, incl. bulk_load.py and calculate_risk.py
.github/skills Development skills (backend and frontend)
```

## Architecture

| File | Responsibility |
|---|---|
| `repository.py` | All SQL |
| `service.py` | Business rules |
| `main.py` | Request/response handling |
| `model.py` | Pydantic request/response models |

## Quick start

See [docs/SETUP.md](docs/SETUP.md). Short version:

```powershell
pip install -r backend/requirements.txt
cd backend\src
python -m uvicorn main:app --reload
```

## Development workflow

1. Write the endpoint spec in [docs/API.md](docs/API.md) with status `Planned`.
2. Backend: implement from the spec using the `care-api-backend` skill.
3. Frontend: implement the interface and fetch script using the `care-frontend-api-client` skill.

Skills live in `.github/skills/`.
