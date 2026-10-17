# API Spec

Source of truth for every endpoint. Write the spec here first with status `Planned`; the backend implements it, then the frontend.
Base URL: `http://127.0.0.1:8000`

## How to add an endpoint
Copy the template, fill every section, set status `Planned`.

```
## <METHOD> <path>
Status: Planned | Backend done | Done
Purpose: <one line>
Request: <query params with defaults/limits, or body>
Response: <example JSON + field table (type, nullable, allowed values)>
Data source: <table.columns>
Business rules: <filters, ordering, calculations, validation>
Errors: <status code and condition>
```

Conventions:
- List endpoints take `limit` (default 100, 1-1000) and `offset` (default 0) and return `{total, limit, offset, items}`.
- `risk_level`: `Low` | `Medium` | `High`. `readmitted`: `NO` | `<30` | `>30`.
- Rates are percentages rounded to 1 decimal.

---

## GET /encounters
Status: Done
Purpose: Page through all encounters.
Request: `limit`, `offset`
Response: `EncounterList`

```json
{
  "total": 101766, "limit": 5, "offset": 0,
  "items": [{
    "encounter_id": 2278392, "patient_nbr": 8222157, "age": "[0-10)",
    "time_in_hospital": 1, "number_inpatient": 0, "number_emergency": 0,
    "number_outpatient": 0, "num_medications": 1, "readmitted": "NO",
    "risk_score": 0.0, "risk_level": "Low"
  }]
}
```

| Field | Type | Nullable |
|---|---|---|
| encounter_id, patient_nbr | int | no |
| age | string | yes |
| time_in_hospital, number_inpatient, number_emergency, number_outpatient, num_medications | int | yes |
| readmitted | string | yes |
| risk_score | float | yes |
| risk_level | string | yes |

Data source: `patient_encounters`
Business rules: ordered by `encounter_id`; page size capped at 1000.
Errors: 422 for invalid `limit`/`offset`.

## GET /encounters/{encounter_id}
Status: Done
Purpose: One encounter.
Request: path `encounter_id` (int)
Response: a single `Encounter` (same fields as an item above).
Data source: `patient_encounters`
Errors: 404 `Encounter {id} not found`; 422 for a non-integer id.

## GET /care-queue
Status: Done
Purpose: Patients who may need attention (Medium and High risk).
Request: `limit`, `offset`
Response: `EncounterList` (same shape as `/encounters`), `risk_level` is `Medium` or `High`.
Data source: `patient_encounters`
Business rules: `risk_level` in (Medium, High); High first, then `risk_score` descending, then `encounter_id`.

## GET /care-queue/high
Status: Done
Purpose: Only the High risk queue.
Request: `limit`, `offset`
Response:

```json
{
  "total": 2358, "limit": 2, "offset": 0,
  "items": [{
    "encounter_id": 67162368, "patient_nbr": 84002391, "age": "[50-60)",
    "readmitted": "<30", "risk_score": 8.0, "risk_level": "High"
  }]
}
```

Fields per item: `encounter_id` int, `patient_nbr` int, `age` string|null, `readmitted` string|null, `risk_score` float|null, `risk_level` string|null.
Data source: `patient_encounters`
Business rules: `risk_level = 'High'`, ordered by `risk_score` descending, then `encounter_id`.

## PATCH /interventions/{encounter_id}
Status: Done
Purpose: Record a human action on a queued encounter.
Request: path `encounter_id`; body (all fields optional):

```json
{ "status": "CONTACTED", "assigned_to": "Care Team A", "notes": "Follow-up initiated" }
```

Response:

```json
{
  "intervention_id": 2, "encounter_id": 35754, "status": "Contacted",
  "assigned_to": "Care Team A", "notes": "Follow-up initiated"
}
```

Data source: `care_interventions`
Business rules:
- `status` is matched case-insensitively against Open, Contacted, In Progress, Completed, Cancelled and stored title-cased.
- Updates the latest intervention for the encounter; creates one (default status `Open`) if none exists.
- Omitted fields keep their current value.

Errors: 404 unknown encounter; 422 invalid status.

## GET /operations/summary
Status: Done
Purpose: Headline counts for operations.
Request: none
Response:

```json
{ "total_encounters": 101766, "high_risk": 2358, "medium_risk": 6180, "pending_reviews": 8537 }
```

All fields int.
Data source: `patient_encounters`, `care_interventions`
Business rules: pending review = Medium/High encounter with no intervention whose status is not `Open`.

## GET /operations/readmission-analysis
Status: Done
Purpose: Compare risk prioritization with historical readmission outcomes.
Request: none
Response:

```json
{
  "overall": { "total_encounters": 101766, "readmitted_30": 11357, "readmission_30_rate": 11.2 },
  "by_risk_level": [
    { "risk_level": "High", "encounters": 2358, "readmitted_30": 674, "readmission_30_rate": 28.6,
      "readmitted_any": 1856, "readmission_any_rate": 78.7, "lift": 2.55 }
  ],
  "care_queue": {
    "queue_size": 8538, "queue_readmitted_30": 2009, "queue_capture_rate": 17.7,
    "queue_readmission_30_rate": 23.5, "lift": 2.1
  }
}
```

`by_risk_level` always has High, Medium and Low in that order (example shows High only).
Data source: `patient_encounters`
Business rules:
- Outcome `readmitted_30` = `readmitted = '<30'`; `readmitted_any` = `readmitted <> 'NO'`.
- `lift` = level (or queue) `<30` rate divided by the overall `<30` rate.
- `queue_capture_rate` = share of all `<30` readmissions that are in the Medium/High queue.
