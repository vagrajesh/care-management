"""Request/response handling. Run: uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

import service
from model import Encounter, EncounterList, Intervention, InterventionUpdate, OperationsSummary, QueueList, ReadmissionAnalysis

app = FastAPI(title="Care Management API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/encounters", response_model=EncounterList)
def get_encounters(
    limit: int = Query(service.DEFAULT_LIMIT, ge=1, le=service.MAX_LIMIT),
    offset: int = Query(0, ge=0),
):
    return service.list_encounters(limit, offset)


@app.get("/encounters/{encounter_id}", response_model=Encounter)
def get_encounter(encounter_id: int):
    try:
        return service.get_encounter(encounter_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/patients/{patient_nbr}/encounters", response_model=EncounterList)
def get_patient_encounters(
    patient_nbr: int,
    limit: int = Query(service.DEFAULT_LIMIT, ge=1, le=service.MAX_LIMIT),
    offset: int = Query(0, ge=0),
):
    try:
        return service.list_patient_encounters(patient_nbr, limit, offset)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/care-queue", response_model=EncounterList)
def get_care_queue(
    limit: int = Query(service.DEFAULT_LIMIT, ge=1, le=service.MAX_LIMIT),
    offset: int = Query(0, ge=0),
):
    return service.list_care_queue(limit, offset)


@app.get("/care-queue/high", response_model=QueueList)
def get_high_risk_queue(
    limit: int = Query(service.DEFAULT_LIMIT, ge=1, le=service.MAX_LIMIT),
    offset: int = Query(0, ge=0),
):
    return service.list_high_risk_queue(limit, offset)


@app.get("/operations/readmission-analysis", response_model=ReadmissionAnalysis)
def get_readmission_analysis():
    return service.readmission_analysis()


@app.get("/operations/summary", response_model=OperationsSummary)
def get_operations_summary():
    return service.operations_summary()


@app.get("/interventions/{encounter_id}", response_model=Intervention)
def get_intervention(encounter_id: int):
    try:
        return service.get_intervention(encounter_id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.patch("/interventions/{encounter_id}", response_model=Intervention)
def patch_intervention(encounter_id: int, body: InterventionUpdate):
    try:
        return service.update_intervention(
            encounter_id, body.status, body.assigned_to, body.notes
        )
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
