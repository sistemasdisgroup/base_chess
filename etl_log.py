from datetime import datetime
from sqlalchemy import text


def insertar_log(
    engine,
    proceso: str,
    distribuidora: str,
    tabla: str,
    filas: int,
    estado: str,
    mensaje: str,
    fecha_inicio: datetime,
    fecha_fin: datetime | None = None,
):
    if fecha_fin is None:
        fecha_fin = datetime.now()

    query = text("""
        INSERT INTO staging.etl_log
        (proceso, distribuidora, tabla, filas, estado, mensaje, fecha_inicio, fecha_fin)
        VALUES
        (:proceso, :distribuidora, :tabla, :filas, :estado, :mensaje, :fecha_inicio, :fecha_fin)
    """)

    with engine.begin() as conn:
        conn.execute(query, {
            "proceso": proceso,
            "distribuidora": distribuidora,
            "tabla": tabla,
            "filas": filas,
            "estado": estado,
            "mensaje": mensaje,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        })