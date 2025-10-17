from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import schemas, models, crud
from .utils import ensure_operators
from fastapi.responses import Response
from .report import build_pdf
from fastapi.staticfiles import StaticFiles
import os
import pandas as pd

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MSA API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/studies", response_model=schemas.StudyOut)
def create_study(payload: schemas.StudyCreate, db: Session = Depends(get_db)):
    try:
        ensure_operators([payload.operator_a, payload.operator_b, payload.operator_c])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    study = crud.create_study(db, payload)
    return study

@app.get("/studies", response_model=list[schemas.StudyOut])
def list_studies(db: Session = Depends(get_db)):
    return crud.list_studies(db)

@app.get("/studies/{study_id}", response_model=schemas.StudyOut)
def get_study(study_id: int, db: Session = Depends(get_db)):
    study = crud.get_study(db, study_id)
    if not study:
        raise HTTPException(status_code=404, detail="Study not found")
    return study

@app.post("/studies/{study_id}/analyze")
def analyze_study(study_id: int, method: str = Query("anova", enum=["anova","range"]), db: Session = Depends(get_db)):
    study = crud.get_study(db, study_id)
    if not study:
        raise HTTPException(status_code=404, detail="Study not found")

    rows = [{
        "sample_index": m.sample_index,
        "series_index": m.series_index,
        "operator_name": m.operator_name,
        "value": m.value,
    } for m in study.measurements]

    if len(rows) == 0:
        raise HTTPException(status_code=400, detail="Brak danych pomiarowych w badaniu.")

    df = pd.DataFrame(rows)

    if method == "range":
        from .analysis_range import average_range_method
        return average_range_method(df, lsl=study.lsl, usl=study.usl)
    else:
        from .analysis import analyze_grr_crossed
        return analyze_grr_crossed(df, lsl=study.lsl, usl=study.usl)

@app.get("/studies/{study_id}/report.pdf")
def report_pdf(study_id: int, method: str = Query("anova", enum=["anova","range"]), db: Session = Depends(get_db)):
    study = crud.get_study(db, study_id)
    if not study:
        raise HTTPException(status_code=404, detail="Study not found")

    rows = [{
        "sample_index": m.sample_index,
        "series_index": m.series_index,
        "operator_name": m.operator_name,
        "value": m.value,
    } for m in study.measurements]

    if len(rows) == 0:
        raise HTTPException(status_code=400, detail="Brak danych pomiarowych w badaniu.")

    df = pd.DataFrame(rows)
    if method == "range":
        from .analysis_range import average_range_method
        analysis = average_range_method(df, lsl=study.lsl, usl=study.usl)
    else:
        from .analysis import analyze_grr_crossed
        analysis = analyze_grr_crossed(df, lsl=study.lsl, usl=study.usl)

    pdf_bytes = build_pdf(study, analysis)
    return Response(content=pdf_bytes, media_type="application/pdf")

# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
