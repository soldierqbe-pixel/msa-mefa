from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Study(Base):
    __tablename__ = "studies"
    id = Column(Integer, primary_key=True, index=True)

    date = Column(String, nullable=False)  # YYYY-MM-DD
    part_name = Column(String, nullable=False)
    caliper_number = Column(String, nullable=False)
    nominal_value = Column(Float, nullable=False)
    lsl = Column(Float, nullable=True)
    usl = Column(Float, nullable=True)

    test_lead = Column(String, nullable=False)
    operator_a = Column(String, nullable=False)
    operator_b = Column(String, nullable=False)
    operator_c = Column(String, nullable=False)

    num_samples = Column(Integer, default=10)
    num_series = Column(Integer, default=3)

    measurements = relationship("Measurement", back_populates="study", cascade="all, delete-orphan")

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    study_id = Column(Integer, ForeignKey("studies.id"), nullable=False)

    sample_index = Column(Integer, nullable=False)   # 1..10
    series_index = Column(Integer, nullable=False)   # 1..3
    operator_name = Column(String, nullable=False)   # one of the 3 operators
    value = Column(Float, nullable=False)

    study = relationship("Study", back_populates="measurements")
