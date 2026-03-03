from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.empresas import router as empresas_router
from routes.obligaciones import router as obligaciones_router
from routes.auth import router as auth_router

app = FastAPI(title="LexControl RH API")

# 🔥 CONFIGURACIÓN CORS
origins = [
    "http://localhost:5173",  # React en desarrollo
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(empresas_router)
app.include_router(obligaciones_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {"mensaje": "LexControl RH API funcionando 🚀"}