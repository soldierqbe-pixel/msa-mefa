from sqlalchemy.orm import Session
from . import models, schemas

def create_study(db: Session, payload: schemas.StudyCreate) -> models.Study:
    study = models.Study(
        date=payload.date,
        part_name=payload.part_name,
        caliper_number=payload.caliper_number,
        nominal_value=payload.nominal_value,
        lsl=payload.lsl,
        usl=payload.usl,
        test_lead=payload.test_lead,
        operator_a=payload.operator_a,
        operator_b=payload.operator_b,
        operator_c=payload.operator_c,
        num_samples=payload.num_samples,
        num_series=payload.num_series,
    )
    db.add(study)
    db.flush()  # get study.id

    for m in payload.measurements:
        db.add(models.Measurement(
            study_id=study.id,
            sample_index=m.sample_index,
            series_index=m.series_index,
            operator_name=m.operator_name,
            value=m.value,
        ))

    db.commit()
    db.refresh(study)
    return study

def get_study(db: Session, study_id: int) -> models.Study | None:
    return db.query(models.Study).filter(models.Study.id == study_id).first()

def list_studies(db: Session):
    return db.query(models.Study).order_by(models.Study.id.desc()).all()
