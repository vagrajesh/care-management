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


def get_intervention(encounter_id):
    if not repository.encounter_exists(encounter_id):
        raise LookupError(f"Encounter {encounter_id} not found")
    intervention = repository.get_intervention(encounter_id)
    if intervention is None:
        raise LookupError(f"No intervention for encounter {encounter_id}")
    return intervention


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


def get_encounter(encounter_id):
    encounter = repository.get_encounter(encounter_id)
    if encounter is None:
        raise LookupError(f"Encounter {encounter_id} not found")
    return encounter


def list_high_risk_queue(limit=DEFAULT_LIMIT, offset=0):
    limit = max(1, min(limit, MAX_LIMIT))
    offset = max(0, offset)
    return {
        "total": repository.count_by_risk_levels(("High",)),
        "limit": limit,
        "offset": offset,
        "items": repository.list_queue_by_level("High", limit, offset),
    }


def _rate(part, whole):
    return round(100.0 * part / whole, 1) if whole else 0.0


def _lift(rate, baseline):
    return round(rate / baseline, 2) if baseline else 0.0


def readmission_analysis():
    """Compare risk prioritization with historical readmission outcomes."""
    counts = {
        level: (enc, r30, rany)
        for level, enc, r30, rany in repository.readmission_counts_by_level()
    }
    total = sum(c[0] for c in counts.values())
    total_30 = sum(c[1] for c in counts.values())
    baseline = _rate(total_30, total)

    by_level = []
    for level in ("High", "Medium", "Low"):
        enc, r30, rany = counts.get(level, (0, 0, 0))
        rate_30 = _rate(r30, enc)
        by_level.append({
            "risk_level": level,
            "encounters": enc,
            "readmitted_30": r30,
            "readmission_30_rate": rate_30,
            "readmitted_any": rany,
            "readmission_any_rate": _rate(rany, enc),
            "lift": _lift(rate_30, baseline),
        })

    queue = [counts.get(level, (0, 0, 0)) for level in CARE_QUEUE_LEVELS]
    queue_size = sum(c[0] for c in queue)
    queue_30 = sum(c[1] for c in queue)
    queue_rate = _rate(queue_30, queue_size)
    return {
        "overall": {
            "total_encounters": total,
            "readmitted_30": total_30,
            "readmission_30_rate": baseline,
        },
        "by_risk_level": by_level,
        "care_queue": {
            "queue_size": queue_size,
            "queue_readmitted_30": queue_30,
            "queue_capture_rate": _rate(queue_30, total_30),
            "queue_readmission_30_rate": queue_rate,
            "lift": _lift(queue_rate, baseline),
        },
    }


def list_patient_encounters(patient_nbr, limit=DEFAULT_LIMIT, offset=0):
    limit = max(1, min(limit, MAX_LIMIT))
    offset = max(0, offset)
    total = repository.count_by_patient(patient_nbr)
    if total == 0:
        raise LookupError(f"Patient {patient_nbr} not found")
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": repository.list_by_patient(patient_nbr, limit, offset),
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
