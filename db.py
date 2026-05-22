from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import text
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
import csv
from io import StringIO
from sqlalchemy import text


def get_engine():
    url = URL.create(
        "postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )

    return create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=1800,
        use_insertmanyvalues=False
    )

def delete_by_date_range(
    engine,
    table_name: str,
    distribuidora: str,
    fecha_desde: str,
    fecha_hasta: str,
    date_column: str,
    schema: str = "staging"
):
    query = text(f'''
        DELETE FROM {schema}.{table_name}
        WHERE distribuidora = :distribuidora
        AND "{date_column}"::date BETWEEN :fecha_desde AND :fecha_hasta
    ''')

    with engine.begin() as conn:
        result = conn.execute(query, {
            "distribuidora": distribuidora,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
        })

    print(f"[DELETE] {schema}.{table_name}: {result.rowcount} filas eliminadas")

def load_table(df, table_name: str, engine, schema: str = "staging", if_exists: str = "append"):
    if df is None or df.empty:
        print(f"[WARN] {schema}.{table_name}: sin datos")
        return 0

    with engine.begin() as conn:
        if if_exists == "replace":
            conn.execute(text(f'TRUNCATE TABLE {schema}."{table_name}"'))

    # Convertir NaN/NaT a NULL compatible con COPY
    df = df.where(df.notnull(), None)

    buffer = StringIO()

    df.to_csv(
        buffer,
        index=False,
        header=False,
        sep="\t",
        na_rep="\\N",
        quoting=csv.QUOTE_MINIMAL
    )

    buffer.seek(0)

    with engine.begin() as conn:
        existing_cols = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = :schema
              AND table_name = :table_name
        """), {
            "schema": schema,
            "table_name": table_name
        }).fetchall()

        existing_cols = {row[0] for row in existing_cols}

        for col in df.columns:
            if col not in existing_cols:
                conn.execute(text(f'ALTER TABLE {schema}."{table_name}" ADD COLUMN "{col}" text'))
                print(f"[ALTER] agregada columna {schema}.{table_name}.{col}")

    columns = ', '.join([f'"{col}"' for col in df.columns])

    copy_sql = f'''
        COPY {schema}."{table_name}" ({columns})
        FROM STDIN
        WITH (
            FORMAT csv,
            DELIMITER E'\\t',
            NULL '\\N',
            QUOTE '"'
        )
    '''

    raw_conn = engine.raw_connection()

    try:
        cursor = raw_conn.cursor()
        cursor.copy_expert(copy_sql, buffer)
        raw_conn.commit()
        cursor.close()
    except Exception:
        raw_conn.rollback()
        raise
    finally:
        raw_conn.close()

    filas = len(df)
    print(f"[OK] {schema}.{table_name}: {filas} filas")
    return filas