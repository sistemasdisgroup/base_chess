from datetime import date, timedelta

from config import SOURCES
from db import get_engine, delete_by_date_range
from runner_utils import cargar_resultado_con_log

from loaders.ventas import extract_ventas
from loaders.ventas_detalle import extract_ventas_detalle


def main():
    engine = get_engine()

    hoy = date.today()
    fecha_desde = (hoy - timedelta(days=30)).isoformat()
    fecha_hasta = hoy.isoformat()

    for source in SOURCES:
        print(f"\nProcesando ventas: {source['nombre']}")
        print(f"Rango: {fecha_desde} a {fecha_hasta}")

        delete_by_date_range(
            engine=engine,
            table_name="ventas",
            distribuidora=source["nombre"],
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            date_column="fechaComprobate"
        )

        delete_by_date_range(
            engine=engine,
            table_name="ventas_detalle",
            distribuidora=source["nombre"],
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            date_column="fechaComprobate"
        )

        result_ventas = extract_ventas(
            source,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            detallado=False
        )

        cargar_resultado_con_log(
            result_ventas,
            engine,
            source,
            proceso="ventas",
            modo="append"
        )

        result_ventas_detalle = extract_ventas_detalle(
            source,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )

        cargar_resultado_con_log(
            result_ventas_detalle,
            engine,
            source,
            proceso="ventas_detalle",
            modo="append"
        )


if __name__ == "__main__":
    main()