from pydantic import BaseModel

class Dev(BaseModel):
    id: int
    name: str
    role: str
    skills: list[str]
    description: str