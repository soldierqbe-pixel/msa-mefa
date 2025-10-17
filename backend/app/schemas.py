from typing import List, Optional
from pydantic import BaseModel, Field

class MeasurementIn(BaseModel):
    sample_index: int
    series_index: int
    operator_name: str
    value: float

class StudyCreate(BaseModel):
    date: str = Field(..., description="YYYY-MM-DD")
    part_name: str
    caliper_number: str
    nominal_value: float
    lsl: Optional[float] = None
    usl: Optional[float] = None

    test_lead: str
    operator_a: str
    operator_b: str
    operator_c: str

    num_samples: int = 10
    num_series: int = 3

    measurements: List[MeasurementIn] = []

class StudyOut(BaseModel):
    id: int
    date: str
    part_name: str
    caliper_number: str
    nominal_value: float
    lsl: Optional[float]
    usl: Optional[float]
    test_lead: str
    operator_a: str
    operator_b: str
    operator_c: str
    num_samples: int
    num_series: int

    class Config:
        from_attributes = True
