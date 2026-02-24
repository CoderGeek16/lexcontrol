from pydantic import BaseModel
from datetime import date
from typing import Optional


class ObligacionBase(BaseModel):
    tipo_obligacion_id: int
    periodo: str
    fecha_vencimiento: date
    estado: str
    monto: float


class ObligacionCreate(ObligacionBase):
    pass


class ObligacionUpdateEstado(BaseModel):
    nuevo_estado: str


class ObligacionResponse(BaseModel):
    id: int
    tipo_obligacion: str
    periodo: str
    fecha_vencimiento: date
    estado: str
    monto: Optional[float]

    class Config:
        from_attributes = True