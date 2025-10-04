# app/main.py
from fastapi import FastAPI
from .database import engine
from .models import patient, clinician 
# --- Import the new router ---
from .routers import patients, auth 

patient.Base.metadata.create_all(bind=engine)
clinician.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Epilepsy Management Platform API")

# --- Include both routers ---
app.include_router(auth.router)
app.include_router(patients.router)

@app.get("/")
def read_root():
    return {"status": "API is running"}