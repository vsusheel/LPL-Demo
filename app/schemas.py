from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from uuid import UUID
from datetime import datetime

class Manufacturer(BaseModel):
    name: str
    homePage: Optional[HttpUrl] = None
    phone: Optional[str] = None

class InventoryItem(BaseModel):
    id: UUID
    name: str
    releaseDate: datetime
    manufacturer: Manufacturer 

class UserAddBody(BaseModel):
    username: str
    password: str
    email: Optional[str] = None 