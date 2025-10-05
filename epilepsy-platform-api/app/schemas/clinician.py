# app/schemas/clinician.py

from pydantic import BaseModel, EmailStr, Field, ConfigDict # <-- Import ConfigDict
from datetime import datetime

class ClinicianCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class Clinician(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # --- Use model_config instead of class Config ---
    model_config = ConfigDict(from_attributes=True)