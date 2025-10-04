# app/routers/patients.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models
from ..schemas.patient import Patient, PatientCreate, PatientUpdate 
from ..dependencies import get_db

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.post("/", response_model=Patient, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    # Corrected: Changed models.Patient to models.patient.Patient
    db_patient = models.patient.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/", response_model=List[Patient])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Corrected: Changed models.Patient to models.patient.Patient
    patients = db.query(models.patient.Patient).offset(skip).limit(limit).all()
    return patients

@router.get("/{patient_id}", response_model=Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    # Corrected: Changed models.Patient to models.patient.Patient
    db_patient = db.query(models.patient.Patient).filter(models.patient.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.put("/{patient_id}", response_model=Patient)
def update_patient(patient_id: int, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    # Corrected: Changed models.Patient to models.patient.Patient
    db_patient = db.query(models.patient.Patient).filter(models.patient.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    update_data = patient_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_patient, key, value)
        
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    # Corrected: Changed models.Patient to models.patient.Patient
    db_patient = db.query(models.patient.Patient).filter(models.patient.Patient.id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(db_patient)
    db.commit()
    return None