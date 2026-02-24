from fastapi import APIRouter, Depends, HTTPException, status
from database import get_connection, release_connection
from core.security import require_role
from schemas.obligacion import (
    ObligacionCreate,
    ObligacionUpdateEstado,
    ObligacionResponse
)

router = APIRouter(prefix="/obligaciones", tags=["Obligaciones"])


@router.get("/", response_model=list[ObligacionResponse])
def listar_obligaciones(
    current_user: dict = Depends(require_role(["admin", "contador", "operador"]))
):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = """
            SELECT 
                o.id,
                t.nombre,
                o.periodo,
                o.fecha_vencimiento,
                o.estado,
                o.monto,
                o.created_at,
                o.updated_at
            FROM obligaciones o
            JOIN tipos_obligacion t 
                ON o.tipo_obligacion_id = t.id
            WHERE o.empresa_id = %s
            AND o.deleted_at IS NULL
            ORDER BY o.periodo;
        """

        cursor.execute(query, (current_user["empresa_id"],))
        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "tipo_obligacion": row[1],
                "periodo": row[2],
                "fecha_vencimiento": row[3],
                "estado": row[4],
                "monto": row[5],
                "created_at": row[6],
                "updated_at": row[7]
            }
            for row in rows
        ]

    finally:
        cursor.close()
        release_connection(conn)