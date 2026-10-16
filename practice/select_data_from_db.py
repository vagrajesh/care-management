from database_conn import get_connection

with get_connection() as conn:
    rows = conn.execute("SELECT * FROM patient_encounters LIMIT 5").fetchall()
    for row in rows:
        print(row)  