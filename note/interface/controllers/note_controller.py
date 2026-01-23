from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/notes")
class NoteResponse(BaseModel):
    pass