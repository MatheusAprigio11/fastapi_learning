from typing import Optional
from pydantic import BaseModel


class Time(BaseModel):
    id: Optional[int] = None
    posicao: int
    time: str
    pontos: int
    vitorias: int