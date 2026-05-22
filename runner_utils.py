from datetime import datetime
from db import load_table
from etl_log import insertar_log


def cargar_resultado_con_log(
    result: dict,
    engine,
    source: dict,
    proceso: str,
    modo: str,
):
    for table_name, df in result.items():
        fecha_inicio = datetime.now()

        try:
            filas = load_table(
                df,
                table_name,
                engine,
                schema="staging",
                if_exists=modo
            )

            insertar_log(
                engine=engine,
                proceso=proceso,
                distribuidora=source["nombre"],
                tabla=table_name,
                filas=filas,
                estado="OK",
                mensaje="Carga correcta",
                fecha_inicio=fecha_inicio,
            )

        except Exception as e:
            insertar_log(
                engine=engine,
                proceso=proceso,
                distribuidora=source["nombre"],
                tabla=table_name,
                filas=0,
                estado="ERROR",
                mensaje=str(e)[:1000],
                fecha_inicio=fecha_inicio,
            )

            raise