"""Business rules for encounters."""
import repository

DEFAULT_LIMIT = 100
MAX_LIMIT = 1000


def operations_summary():
    total, high, medium, pending = repository.operations_summary()
    return {
        "total_encounters": total,
        "high_risk": high,
        "medium_risk": medium,
        "pending_reviews": pending,
    }
VALID_STATUSES = {
    "OPEN": "Open",
    "CONTACTED": "Contacted",
    "IN PROGRESS": "In Progress",
    "COMPLETED": "Completed",
    "CANCELLED": "Cancelled",
}


def update_intervention(encounter_id, status=None, assigned_to=None, notes=None):
    if status is not None:
        normalized = VALID_STATUSES.get(status.strip().upper())
        if normalized is None:
            raise ValueError(f"status must be one of {sorted(VALID_STATUSES.values())}")
        status = normalized
    if not repository.encounter_exists(encounter_id):
        raise LookupError(f"Encounter {encounter_id} not found")
    return repository.update_intervention(encounter_id, status, assigned_to, notes)
CARE_QUEUE_LEVELS = ("Medium", "High")


def list_care_queue(limit=DEFAULT_LIMIT, offset=0):
    # Care team only sees patients who may need attention, High first
    limit = max(1, min(limit, MAX_LIMIT))
    offset = max(0, offset)
    return {
        "total": repository.count_by_risk_levels(CARE_QUEUE_LEVELS),
        "limit": limit,
        "offset": offset,
        "items": repository.list_by_risk_levels(CARE_QUEUE_LEVELS, limit, offset),
    }


def list_encounters(limit=DEFAULT_LIMIT, offset=0):
    # Cap page size so one request can't pull the whole table
    limit = max(1, min(limit, MAX_LIMIT))
    offset = max(0, offset)
    return {
        "total": repository.count_encounters(),
        "limit": limit,
        "offset": offset,
        "items": repository.list_encounters(limit, offset),
    }
