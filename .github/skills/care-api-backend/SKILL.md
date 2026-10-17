---
name: care-api-backend
description: Implements a new or changed FastAPI endpoint for the care-management backend from its spec in docs/API.md. Use when adding or modifying an endpoint, repository query, service rule, or Pydantic model in backend/src.
---

# Care API backend

The endpoint spec in `docs/API.md` is the source of truth. Implement exactly what it says. If the spec is incomplete or ambiguous, ask the user instead of guessing.

## Layer rules (backend/src)

| File | Owns | Must not contain |
|---|---|---|
| `repository.py` | All SQL. `%s` placeholders only. Convert NUMERIC `risk_score` to `float`. | Business rules, HTTP |
| `service.py` | Business rules: limit/offset caps, validation, rate/lift math, constants (e.g. `CARE_QUEUE_LEVELS`, `VALID_STATUSES`). Raise `LookupError` (not found) and `ValueError` (invalid input). | SQL, FastAPI imports |
| `main.py` | Routes, `Query` validation, `response_model`, mapping `LookupError` to 404 and `ValueError` to 422. | SQL, business logic |
| `model.py` | Every Pydantic request/response model. | Anything else |

## Database (database_conn.py)
- Always use `get_connection()`. Never open connections elsewhere.
- Use `with get_connection() as conn`; it commits on a clean exit.
- `DATABASE_URL` comes from `.env`. Never commit or print it.
- The app user cannot `ALTER` tables. Give schema changes to the user as SQL to run as the owner, and update `db/schema.sql`.

## Steps for each endpoint
1. Read the endpoint in `docs/API.md`, and `db/schema.sql` for real columns and constraints. Confirm the columns exist.
2. `repository.py`: add the query.
3. `service.py`: add the business rules.
4. `model.py`: add the response (and request) models matching the spec's fields and nullability.
5. `main.py`: add the route. Place fixed paths before `/{id}` routes.
6. Test with `fastapi.testclient.TestClient` from `backend/src`: the success case and each documented error. Compare the response with the spec example.
7. Set the endpoint's status to `Backend done` in `docs/API.md`; fix the spec only if the user agrees it changed.
8. Delete `__pycache__` created by test runs.

See `docs/SETUP.md` for environment and running the server (`python -m uvicorn main:app --reload` from `backend/src`).
