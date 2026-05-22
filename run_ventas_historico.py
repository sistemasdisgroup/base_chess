from datetime import date
from dateutil.relativedelta import relativedelta

from config import SOURCES
from db import get_engine, delete_by_date_range
from runner_utils import cargar_resultado_con_log

from loaders.ventas import extract_ventas
from loaders.ventas_detalle import extract_ventas_detalle


FECHA_INICIO = date(2026, 1, 1)
FECHA_FIN = date.today()


def meses_entre(fecha_inicio: date, fecha_fin: date):
    actual = fecha_inicio.replace(day=1)

    while actual <= fecha_fin:
        siguiente_mes = actual + relativedelta(months=1)
        fin_mes = siguiente_mes - relativedelta(days=1)

        if fin_mes > fecha_fin:
            fin_mes = fecha_fin

        yield actual.isoformat(), fin_mes.isoformat()

        actual = siguiente_mes


def main():
    engine = get_engine()

    for fecha_desde, fecha_hasta in meses_entre(FECHA_INICIO, FECHA_FIN):
        print(f"\n===== Procesando histórico {fecha_desde} a {fecha_hasta} =====")

        for source in SOURCES:
            print(f"\nDistribuidora: {source['nombre']}")

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
                proceso="ventas_historico",
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
                proceso="ventas_detalle_historico",
                modo="append"
            )


if __name__ == "__main__":
    main()
