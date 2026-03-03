from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database import get_connection, release_connection
from core.security import require_role


router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)


# =========================
# SCHEMAS
# =========================

class EmpresaCreate(BaseModel):
    nombre: str
    ruc: str


class EmpresaUpdate(BaseModel):
    nombre: str
    ruc: str


# =========================
# LISTAR EMPRESAS
# =========================

@router.get("/")
def listar_empresas(
    current_user: dict = Depends(require_role(["admin"]))
):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, nombre, ruc FROM empresas")
        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "nombre": row[1],
                "ruc": row[2]
            }
            for row in rows
        ]

    finally:
        cursor.close()
        release_connection(conn)


# =========================
# CREAR EMPRESA
# =========================

@router.post("/")
def crear_empresa(
    empresa: EmpresaCreate,
    current_user: dict = Depends(require_role(["admin"]))
):

    if len(empresa.ruc) != 11 or not empresa.ruc.isdigit():
        raise HTTPException(
            status_code=400,
            detail="El RUC debe tener exactamente 11 dígitos numéricos"
        )

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM empresas WHERE ruc = %s",
            (empresa.ruc,)
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail="Ya existe una empresa con ese RUC"
            )

        cursor.execute(
            "INSERT INTO empresas (nombre, ruc) VALUES (%s, %s) RETURNING id",
            (empresa.nombre, empresa.ruc)
        )

        nueva_id = cursor.fetchone()[0]
        conn.commit()

        return {
            "id": nueva_id,
            "nombre": empresa.nombre,
            "ruc": empresa.ruc
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear empresa: {str(e)}"
        )

    finally:
        cursor.close()
        release_connection(conn)


# =========================
# ACTUALIZAR EMPRESA
# =========================

@router.put("/{empresa_id}")
def actualizar_empresa(
    empresa_id: int,
    empresa: EmpresaUpdate,
    current_user: dict = Depends(require_role(["admin"]))
):

    if len(empresa.ruc) != 11 or not empresa.ruc.isdigit():
        raise HTTPException(
            status_code=400,
            detail="El RUC debe tener exactamente 11 dígitos numéricos"
        )

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Verificar existencia
        cursor.execute(
            "SELECT id FROM empresas WHERE id = %s",
            (empresa_id,)
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail="Empresa no encontrada"
            )

        # Verificar RUC duplicado en otra empresa
        cursor.execute(
            "SELECT id FROM empresas WHERE ruc = %s AND id != %s",
            (empresa.ruc, empresa_id)
        )
        if cursor.fetchone():
            raise HTTPException(
                status_code=400,
                detail="Otra empresa ya tiene ese RUC"
            )

        cursor.execute(
            """
            UPDATE empresas
            SET nombre = %s,
                ruc = %s
            WHERE id = %s
            """,
            (empresa.nombre, empresa.ruc, empresa_id)
        )

        conn.commit()

        return {
            "message": "Empresa actualizada correctamente"
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar empresa: {str(e)}"
        )

    finally:
        cursor.close()
        release_connection(conn)


# =========================
# ELIMINAR EMPRESA
# =========================

@router.delete("/{empresa_id}")
def eliminar_empresa(
    empresa_id: int,
    current_user: dict = Depends(require_role(["admin"]))
):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM empresas WHERE id = %s",
            (empresa_id,)
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail="Empresa no encontrada"
            )

        cursor.execute(
            "DELETE FROM empresas WHERE id = %s",
            (empresa_id,)
        )

        conn.commit()

        return {
            "message": "Empresa eliminada correctamente"
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al eliminar empresa: {str(e)}"
        )

    finally:
        cursor.close()
        release_connection(conn)