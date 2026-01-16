import psycopg

from psycopg_pool import ConnectionPool
from psycopg import sql
from dotenv import load_dotenv
import os

load_dotenv()

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
                ).format(schema_name, table_name)
            )
            return cur.fetchone()[0]


def create_table(table_name: str, index_name: str):
    if not table_exists("thermostat_readings"):
        with psycopg.connect(conn_str) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    sql.SQL(
                        """CREATE TABLE {} (id serial PRIMARY KEY, temperature_c double precision NOT NULL, humidity integer, hvac_mode text, recorded_at TIMESTAMPTZ NOT NULL DEFAULT now());"""
                    ).format(sql.Identifier(table_name))
                )
                cur.execute(
                    sql.SQL(
                        """CREATE INDEX {}_time ON thermostat_readings (recorded_at);"""
                    ).format(sql.Identifier(index_name))
                )
            conn.commit()
        return "Table Created"
    return "Table already exists"


with psycopg.connect(conn_str) as conn:
    with conn.cursor() as cur:
        print(cur.execute("SELECT to_regclass('public.thermostat_readings')"))


def insert_reading(temp_c: float, humidity: int, hvac_mode: str):
    with psycopg.connect(conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO thermostat_readings (temperature_c, humidity, hvac_mode) VALUES (%s, %s, %s)",
                (temp_c, humidity, hvac_mode),
            )
        conn.commit()


create_table("thermostat_readings", "idx_thermostat")
insert_reading(4.5, 34, "HEATCOOL")
