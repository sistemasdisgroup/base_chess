from config import SOURCES
from db import get_engine
from runner_utils import cargar_resultado_con_log

from loaders.clientes import extract_clientes
from loaders.articulos import extract_articulos
from loaders.lista_precios import extract_lista_precios
from loaders.personal_comercial import extract_personal_comercial
from loaders.rutas_venta import extract_rutas_venta
from loaders.jerarquia_mkt import extract_jerarquia_mkt


def main():
    engine = get_engine()
    primera = True

    for source in SOURCES:
        print(f"\nProcesando maestros: {source['nombre']}")

        modo = "replace" if primera else "append"

        cargar_resultado_con_log(
            extract_clientes(source),
            engine,
            source,
            proceso="maestros_clientes",
            modo=modo
        )

        cargar_resultado_con_log(
            extract_articulos(source),
            engine,
            source,
            proceso="maestros_articulos",
            modo=modo
        )

        cargar_resultado_con_log(
            extract_lista_precios(source),
            engine,
            source,
            proceso="maestros_lista_precios",
            modo=modo
        )

        cargar_resultado_con_log(
            extract_personal_comercial(source),
            engine,
            source,
            proceso="maestros_personal_comercial",
            modo=modo
        )

        cargar_resultado_con_log(
            extract_rutas_venta(source),
            engine,
            source,
            proceso="maestros_rutas_venta",
            modo=modo
        )

        cargar_resultado_con_log(
            extract_jerarquia_mkt(source),
            engine,
            source,
            proceso="maestros_jerarquia_mkt",
            modo=modo
        )

        primera = False


if __name__ == "__main__":
    main()