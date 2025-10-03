# app/routers/patients.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models
# --- This is the corrected import line ---
from ..schemas.patient import Patient, PatientCreate 
from ..dependencies import get_db

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

# --- The response_model is now just 'Patient' ---
@router.post("/", response_model=Patient) 
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)): # <-- Also updated here
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# --- The response_model is now 'List[Patient]' ---
@router.get("/", response_model=List[Patient])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    patients = db.query(models.Patient).offset(skip).limit(limit).all()
    return patients