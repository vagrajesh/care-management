-- Run as the table owner (the app user cannot ALTER or create these tables).
-- Replace fde_user with your application database user.

CREATE TABLE IF NOT EXISTS patient_encounters (
    encounter_id      BIGINT PRIMARY KEY,
    patient_nbr       BIGINT NOT NULL,
    age               VARCHAR,
    time_in_hospital  SMALLINT CHECK (time_in_hospital >= 0),
    number_inpatient  SMALLINT DEFAULT 0 CHECK (number_inpatient >= 0),
    number_emergency  SMALLINT DEFAULT 0 CHECK (number_emergency >= 0),
    number_outpatient SMALLINT DEFAULT 0 CHECK (number_outpatient >= 0),
    num_medications   SMALLINT CHECK (num_medications >= 0),
    readmitted        VARCHAR CHECK (readmitted IN ('NO', '<30', '>30')),
    risk_score        NUMERIC,
    risk_level        VARCHAR CHECK (risk_level IN ('Low', 'Medium', 'High'))
);

CREATE INDEX IF NOT EXISTS idx_patient_encounters_patient_nbr ON patient_encounters (patient_nbr);
CREATE INDEX IF NOT EXISTS idx_patient_encounters_risk_level  ON patient_encounters (risk_level);

CREATE TABLE IF NOT EXISTS care_interventions (
    intervention_id BIGSERIAL PRIMARY KEY,
    encounter_id    BIGINT NOT NULL REFERENCES patient_encounters (encounter_id) ON DELETE CASCADE,
    status          VARCHAR NOT NULL DEFAULT 'Open'
                    CHECK (status IN ('Open', 'Contacted', 'In Progress', 'Completed', 'Cancelled')),
    assigned_to     VARCHAR,
    notes           TEXT
);

CREATE INDEX IF NOT EXISTS idx_care_interventions_encounter_id ON care_interventions (encounter_id);
CREATE INDEX IF NOT EXISTS idx_care_interventions_status       ON care_interventions (status);

-- Application user privileges
GRANT SELECT, INSERT, UPDATE ON patient_encounters TO fde_user;
GRANT SELECT, INSERT, UPDATE ON care_interventions TO fde_user;
GRANT USAGE, SELECT ON SEQUENCE care_interventions_intervention_id_seq TO fde_user;
