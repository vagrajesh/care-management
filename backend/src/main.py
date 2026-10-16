"""Request/response handling. Run: uvicorn main:app --reload"""
from fastapi import FastAPI, HTTPException, Query

import service
from model import EncounterList, Intervention, InterventionUpdate, OperationsSummary

app = FastAPI(title="Care Management API")


@app.get("/encounters", response_model=EncounterList)
def get_encounters(
    limit: int = Query(service.DEFAULT_LIMIT, ge=1, le=service.MAX_LIMIT),
    offset: int = Query(0, ge=0),
):
    return service.list_encounters(limit, offset)


@app.get("/care-queue", response_model=EncounterList)
def get_care_queue(
    limit: int = Query(service.DEFAULT_LIMIT, ge=1, le=service.MAX_LIMIT),
    offset: int = Query(0, ge=0),
):
    return service.list_care_queue(limit, offset)


@app.get("/operations/summary", response_model=OperationsSummary)
def get_operations_summary():
    return service.operations_summary()


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
