from config import SOURCES
from db import get_engine
from runner_utils import cargar_resultado_con_log

from loaders.stock import extract_stock


def main():
    engine = get_engine()
    primera = True

    for source in SOURCES:
        print(f"\nProcesando stock: {source['nombre']}")

        modo = "replace" if primera else "append"

        cargar_resultado_con_log(
            extract_stock(
                source,
                fecha_stock=None,
                frescura=True
            ),
            engine,
            source,
            proceso="stock",
            modo=modo
        )

        primera = False


if __name__ == "__main__":
    main()