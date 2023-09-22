from typing import Optional
from pydantic import BaseModel


class Time(BaseModel):
    id: Optional[int] = None
    time: str
    pontos: int
    posicao: int
    vitorias: int