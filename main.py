from fastapi import FastAPI
from routes.empresas import router as empresas_router
from routes.obligaciones import router as obligaciones_router

app = FastAPI(title="LexControl RH API")

app.include_router(empresas_router)
app.include_router(obligaciones_router)

@app.get("/")
def home():
    return {"mensaje": "LexControl RH API funcionando 🚀"}

from routes.auth import router as auth_router

app.include_router(auth_router)