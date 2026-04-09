from psycopg_pool import ConnectionPool
from psycopg import sql
from dotenv import load_dotenv
import psycopg
import os

load_dotenv()

_required = ["DB_HOST", "DB_USER", "DB_NAME", "DB_PASSWORD", "DB_PORT"]
_missing = [k for k in _required if not os.getenv(k)]
if _missing:
    raise EnvironmentError(f"Missing required environment variables: {', '.join(_missing)}")

conn_str = f"host={os.getenv('DB_HOST')} user={os.getenv('DB_USER')} dbname={os.getenv('DB_NAME')} password={os.getenv('DB_PASSWORD')} port={os.getenv('DB_PORT')}"


def connection():
    with ConnectionPool(conn_str) as pool:
        with pool.connection() as conn:
            return conn


def table_exists(table_name, schema_name="public"):
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:

            cur.execute(
                sql.SQL(
                    "SELECT EXISTS(SELECT FROM pg_tables WHERE schemaname={} AND tablename={});"
                ).format(sql.Literal(schema_name), sql.Literal(table_name))
            )
            row = cur.fetchone()
            return row[0] if row else False


def create_table(table_name: str, index_name: str):
    if not table_exists("thermostat_readings"):
        with psycopg.connect(conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql.SQL(
                        """CREATE TABLE {} (id serial PRIMARY KEY, current_temperature double precision NOT NULL, set_point_heat double precision, set_point_cool double precision, hvac_mode text, status text, recorded_at TIMESTAMPTZ NOT NULL DEFAULT now());"""
                    ).format(sql.Identifier(table_name))
                )
                cur.execute(
                    sql.SQL(
                        """CREATE INDEX {} ON thermostat_readings (recorded_at);"""
                    ).format(sql.Identifier(index_name))
                )
            conn.commit()
        return "Table Created"
    return "Table already exists"


def insert_reading(
    current_temp: float,
    set_point_heat: float,
    set_point_cool: float,
    hvac_mode: str,
    status: str,
):
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO thermostat_readings (current_temperature, set_point_heat, set_point_cool, hvac_mode, status, recorded_at) VALUES (%s, %s, %s, %s, %s, now())",
                (current_temp, set_point_heat, set_point_cool, hvac_mode, status),
            )
        conn.commit()
