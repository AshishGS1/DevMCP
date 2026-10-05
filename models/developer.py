from pydantic import BaseModel
from typing import Any

class Dev(BaseModel):
    id: int
    name: str
    role: str
    skills: list[str]
    description: str

class DevRecord(Dev):
    guid: str

class SimiDev(DevRecord):
    score: float

class SimiSearchResponse(BaseModel):
    records: list[SimiDev]
    count: int

class MultiRecResponse(BaseModel):
    records: list[DevRecord]
    count: int
    next_cursor :str | None = None