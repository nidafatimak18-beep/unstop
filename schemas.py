from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class HCPBase(BaseModel):
    name: str
    specialty: str
    hospital: str
    contact_info: str

class HCPResponse(HCPBase):
    id: int

    class Config:
        from_attributes = True

class InteractionCreate(BaseModel):
    hcp_id: int
    notes: str
    sentiment: Optional[str] = "Neutral"

class InteractionResponse(InteractionCreate):
    id: int
    date: datetime

    class Config:
        from_attributes = True

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
