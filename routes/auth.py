from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from database import get_connection, release_connection
from core.security import hash_password, verify_password, create_access_token
from models.user import UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserCreate):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email ya registrado")

        hashed_password = hash_password(user.password)

        cursor.execute(
            """
            INSERT INTO usuarios (nombre, email, password_hash, rol, empresa_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (user.nombre, user.email, hashed_password, "admin", 1),
        )

        user_id = cursor.fetchone()[0]
        conn.commit()

        return {"message": "Usuario creado correctamente", "user_id": user_id}

    finally:
        cursor.close()
        release_connection(conn)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id, password_hash, empresa_id FROM usuarios WHERE email = %s",
            (form_data.username,),
        )

        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=400, detail="Credenciales inválidas")

        user_id, password_hash_db, empresa_id = result

        if not verify_password(form_data.password, password_hash_db):
            raise HTTPException(status_code=400, detail="Credenciales inválidas")

        access_token = create_access_token({
            "user_id": user_id,
            "empresa_id": empresa_id
        })

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    finally:
        cursor.close()
        release_connection(conn)