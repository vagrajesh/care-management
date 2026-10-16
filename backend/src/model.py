"""Pydantic request/response models."""
from typing import List, Optional

from pydantic import BaseModel


class Encounter(BaseModel):
    encounter_id: int
    patient_nbr: int
    age: Optional[str] = None
    time_in_hospital: Optional[int] = None
    number_inpatient: Optional[int] = None
    number_emergency: Optional[int] = None
    number_outpatient: Optional[int] = None
    num_medications: Optional[int] = None
    readmitted: Optional[str] = None
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None


class EncounterList(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[Encounter]


class InterventionUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    notes: Optional[str] = None


class Intervention(BaseModel):
    intervention_id: int
    encounter_id: int
    status: str
    assigned_to: Optional[str] = None
    notes: Optional[str] = None


class OperationsSummary(BaseModel):
    total_encounters: int
    high_risk: int
    medium_risk: int
    pending_reviews: int
