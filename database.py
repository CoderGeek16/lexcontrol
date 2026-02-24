import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

# Cargar variables desde .env (solo si existe)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception(
        "DATABASE_URL no está configurada como variable de entorno"
    )

# Crear connection pool global
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,   # mínimo de conexiones
        maxconn=10,  # máximo de conexiones simultáneas
        dsn=DATABASE_URL
    )

    if connection_pool:
        print("✅ Connection pool creado correctamente")

except Exception as e:
    raise Exception(f"❌ Error creando connection pool: {e}")


def get_connection():
    """
    Obtiene una conexión del pool
    """
    try:
        return connection_pool.getconn()
    except Exception as e:
        raise Exception(f"Error obteniendo conexión del pool: {e}")


def release_connection(conn):
    """
    Devuelve la conexión al pool
    """
    try:
        connection_pool.putconn(conn)
    except Exception as e:
        raise Exception(f"Error devolviendo conexión al pool: {e}")