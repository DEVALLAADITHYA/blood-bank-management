from pydantic import BaseModel, Field
from datetime import date

class Donor(BaseModel):
    name: str = Field(..., min_length=2)
    blood_group: str
    last_donation: date

class Blood(BaseModel):
    blood_group: str
    units: int = Field(..., gt=0)

class Request(BaseModel):
    patient_name: str
    blood_group: str
    units: int = Field(..., gt=0)
    status: str = "Pending"
