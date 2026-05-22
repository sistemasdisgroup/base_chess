from datetime import date

from config import SOURCES
from db import get_engine
from runner_utils import cargar_resultado_con_log

from loaders.pedidos import extract_pedidos


def main():
    engine = get_engine()
    fecha = date.today().isoformat()

    primera = True

    for source in SOURCES:
        print(f"\nProcesando pedidos: {source['nombre']}")

        modo = "replace" if primera else "append"

        cargar_resultado_con_log(
            extract_pedidos(source, fecha=fecha),
            engine,
            source,
            proceso="pedidos",
            modo=modo
        )

        primera = False


if __name__ == "__main__":
    main()