from pydantic import BaseModel

class EmpresaCreate(BaseModel):
    nombre: str
    ruc: str
    ultimo_digito_ruc: int

class EmpresaResponse(BaseModel):
    id: int
    nombre: str
    ruc: str
    ultimo_digito_ruc: int