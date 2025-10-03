from fastapi import FastAPI
from .database import engine
from .models import patient
from .routers import patients

patient.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Epilepsy Management Platform API")

app.include_router(patients.router)

@app.get("/")
def read_root():
    return {"status": "API is running"}