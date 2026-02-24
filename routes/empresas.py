from fastapi import APIRouter, Depends
from database import get_connection, release_connection
from core.security import require_role

router = APIRouter(prefix="/empresas", tags=["Empresas"])


@router.get("/")
def listar_empresas(current_user: dict = Depends(require_role(["admin"]))):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, nombre FROM empresas")
        rows = cursor.fetchall()

        return [
            {"id": row[0], "nombre": row[1]}
            for row in rows
        ]

    finally:
        cursor.close()
        release_connection(conn)