# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import models, schemas
from ..dependencies import get_db
from ..security import verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["Authentication"])

@router.post("/token", summary="Create access token for user login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    clinician = db.query(models.clinician.Clinician).filter(models.clinician.Clinician.email == form_data.username).first()

    if not clinician or not verify_password(form_data.password, clinician.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": clinician.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/clinicians/", response_model=schemas.clinician.Clinician, status_code=status.HTTP_201_CREATED)
def create_clinician(clinician: schemas.clinician.ClinicianCreate, db: Session = Depends(get_db)):
    db_clinician = db.query(models.clinician.Clinician).filter(models.clinician.Clinician.email == clinician.email).first()
    if db_clinician:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(clinician.password)
    db_clinician = models.clinician.Clinician(email=clinician.email, hashed_password=hashed_password)

    db.add(db_clinician)
    db.commit()
    db.refresh(db_clinician)
    return db_clinician