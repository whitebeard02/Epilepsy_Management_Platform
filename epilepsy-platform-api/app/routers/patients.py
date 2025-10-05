# app/routers/patients.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, security
from ..schemas.patient import Patient, PatientCreate, PatientUpdate
from ..schemas.clinician import Clinician as ClinicianSchema
from ..dependencies import get_db

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.post("/", response_model=Patient, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db), current_clinician: ClinicianSchema = Depends(security.get_current_clinician)):
    # --- Use .model_dump() instead of .dict() ---
    db_patient = models.patient.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/", response_model=List[Patient])
def read_patients(db: Session = Depends(get_db), current_clinician: ClinicianSchema = Depends(security.get_current_clinician)):
    patients = db.query(models.patient.Patient).all()
    return patients

@router.get("/{patient_id}", response_model=Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db), current_clinician: ClinicianSchema = Depends(security.get_current_clinician)):
    db_patient = db.query(models.patient.Patient).filter(models.patient.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.put("/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, patient_update: PatientUpdate, db: Session = Depends(get_db), current_clinician: ClinicianSchema = Depends(security.get_current_clinician)):
    db_patient = db.query(models.patient.Patient).filter(models.patient.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    # --- Use .model_dump() instead of .dict() ---
    update_data = patient_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db), current_clinician: ClinicianSchema = Depends(security.get_current_clinician)):
    db_patient = db.query(models.patient.Patient).filter(models.patient.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(db_patient)
    db.commit()
    return None