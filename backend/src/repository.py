"""All SQL for patient_encounters lives here."""
from database_conn import get_connection

COLUMNS = (
    "encounter_id, patient_nbr, age, time_in_hospital, number_inpatient, "
    "number_emergency, number_outpatient, num_medications, readmitted, "
    "risk_score, risk_level"
)


def list_encounters(limit, offset):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            f"SELECT {COLUMNS} FROM patient_encounters ORDER BY encounter_id LIMIT %s OFFSET %s",
            (limit, offset),
        )
        names = [d.name for d in cur.description]
        rows = [dict(zip(names, r)) for r in cur.fetchall()]
        for r in rows:
            r["risk_score"] = float(r["risk_score"]) if r["risk_score"] is not None else None
        return rows


def get_encounter(encounter_id):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            f"SELECT {COLUMNS} FROM patient_encounters WHERE encounter_id = %s",
            (encounter_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        encounter = dict(zip([d.name for d in cur.description], row))
        if encounter["risk_score"] is not None:
            encounter["risk_score"] = float(encounter["risk_score"])
        return encounter


def list_by_patient(patient_nbr, limit, offset):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            f"SELECT {COLUMNS} FROM patient_encounters WHERE patient_nbr = %s "
            "ORDER BY encounter_id DESC LIMIT %s OFFSET %s",
            (patient_nbr, limit, offset),
        )
        names = [d.name for d in cur.description]
        rows = [dict(zip(names, r)) for r in cur.fetchall()]
        for r in rows:
            r["risk_score"] = float(r["risk_score"]) if r["risk_score"] is not None else None
        return rows


def count_by_patient(patient_nbr):
    with get_connection() as conn:
        return conn.execute(
            "SELECT count(*) FROM patient_encounters WHERE patient_nbr = %s", (patient_nbr,)
        ).fetchone()[0]


def list_by_risk_levels(levels, limit, offset):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            f"SELECT {COLUMNS} FROM patient_encounters WHERE risk_level = ANY(%s) "
            "ORDER BY (risk_level = 'High') DESC, risk_score DESC, encounter_id "
            "LIMIT %s OFFSET %s",
            (list(levels), limit, offset),
        )
        names = [d.name for d in cur.description]
        rows = [dict(zip(names, r)) for r in cur.fetchall()]
        for r in rows:
            r["risk_score"] = float(r["risk_score"]) if r["risk_score"] is not None else None
        return rows


QUEUE_COLUMNS = "encounter_id, patient_nbr, age, readmitted, risk_score, risk_level"


def list_queue_by_level(level, limit, offset):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            f"SELECT {QUEUE_COLUMNS} FROM patient_encounters WHERE risk_level = %s "
            "ORDER BY risk_score DESC, encounter_id LIMIT %s OFFSET %s",
            (level, limit, offset),
        )
        names = [d.name for d in cur.description]
        rows = [dict(zip(names, r)) for r in cur.fetchall()]
        for r in rows:
            r["risk_score"] = float(r["risk_score"]) if r["risk_score"] is not None else None
        return rows


def count_by_risk_levels(levels):
    with get_connection() as conn:
        return conn.execute(
            "SELECT count(*) FROM patient_encounters WHERE risk_level = ANY(%s)",
            (list(levels),),
        ).fetchone()[0]


def encounter_exists(encounter_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT 1 FROM patient_encounters WHERE encounter_id = %s", (encounter_id,)
        ).fetchone() is not None


def get_intervention(encounter_id):
    """Latest intervention for the encounter, or None."""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT intervention_id, encounter_id, status, assigned_to, notes "
            "FROM care_interventions WHERE encounter_id = %s "
            "ORDER BY intervention_id DESC LIMIT 1",
            (encounter_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return dict(zip([d.name for d in cur.description], row))


def update_intervention(encounter_id, status, assigned_to, notes):
    """Update the latest intervention for the encounter; create one if none exists."""
    cols = "intervention_id, encounter_id, status, assigned_to, notes"
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT intervention_id FROM care_interventions "
            "WHERE encounter_id = %s ORDER BY intervention_id DESC LIMIT 1",
            (encounter_id,),
        )
        row = cur.fetchone()
        if row:
            cur.execute(
                "UPDATE care_interventions SET status = COALESCE(%s, status), "
                "assigned_to = COALESCE(%s, assigned_to), notes = COALESCE(%s, notes) "
                f"WHERE intervention_id = %s RETURNING {cols}",
                (status, assigned_to, notes, row[0]),
            )
        else:
            cur.execute(
                "INSERT INTO care_interventions (encounter_id, status, assigned_to, notes) "
                f"VALUES (%s, COALESCE(%s, 'Open'), %s, %s) RETURNING {cols}",
                (encounter_id, status, assigned_to, notes),
            )
        names = [d.name for d in cur.description]
        return dict(zip(names, cur.fetchone()))


def operations_summary():
    # Pending review = Medium/High encounter with no intervention past 'Open'
    with get_connection() as conn:
        return conn.execute(
            "SELECT count(*), "
            "count(*) FILTER (WHERE risk_level = 'High'), "
            "count(*) FILTER (WHERE risk_level = 'Medium'), "
            "count(*) FILTER (WHERE risk_level IN ('High','Medium') AND NOT EXISTS ("
            "  SELECT 1 FROM care_interventions ci "
            "  WHERE ci.encounter_id = pe.encounter_id AND ci.status <> 'Open')) "
            "FROM patient_encounters pe"
        ).fetchone()


def readmission_counts_by_level():
    with get_connection() as conn:
        return conn.execute(
            "SELECT risk_level, count(*), "
            "count(*) FILTER (WHERE readmitted = '<30'), "
            "count(*) FILTER (WHERE readmitted <> 'NO') "
            "FROM patient_encounters GROUP BY risk_level"
        ).fetchall()


def count_encounters():
    with get_connection() as conn:
        return conn.execute("SELECT count(*) FROM patient_encounters").fetchone()[0]
