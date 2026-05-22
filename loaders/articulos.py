from datetime import datetime
import re
import pandas as pd

from api_client import get


def obtener_total_lotes(texto):
    if not texto:
        return 1

    match = re.search(r"(\d+)\s*/\s*(\d+)", str(texto))
    if match:
        return int(match.group(2))

    return 1


def extract_articulos(source: dict):
    data_lote_1 = get(
        base_url=source["base_url"],
        endpoint="articulos/",
        user=source["user"],
        password=source["password"],
        params={"nroLote": 1},
    )

    texto_info = data_lote_1.get("cantArticulos")
    total_lotes = obtener_total_lotes(texto_info)

    print(f"Distribuidora: {source['nombre']}")
    print(f"Info API: {texto_info}")
    print(f"Total lotes articulos: {total_lotes}")

    fecha_carga = datetime.now()

    rows_articulos = []
    rows_agrupaciones = []
    rows_relavacio = []

    for nro_lote in range(1, total_lotes + 1):
        print(f"  -> Lote articulos {nro_lote}/{total_lotes}")

        data = get(
            base_url=source["base_url"],
            endpoint="articulos/",
            user=source["user"],
            password=source["password"],
            params={"nroLote": nro_lote},
        )

        articulos = data.get("Articulos", {}).get("eArticulos", [])

        for art in articulos:
            articulo = art.copy()

            agrupaciones = articulo.pop("eAgrupaciones", [])
            relavacio = articulo.pop("eRelavacio", [])

            articulo["distribuidora"] = source["nombre"]
            articulo["servidor_origen"] = source["base_url"]
            articulo["fecha_carga"] = fecha_carga
            articulo["nro_lote"] = nro_lote

            rows_articulos.append(articulo)

            if agrupaciones:
                for agr in agrupaciones:
                    row = agr.copy()
                    row["distribuidora"] = source["nombre"]
                    row["servidor_origen"] = source["base_url"]
                    row["idArticuloPadre"] = art.get("idArticulo")
                    row["fecha_carga"] = fecha_carga
                    row["nro_lote"] = nro_lote
                    rows_agrupaciones.append(row)

            if relavacio:
                for rel in relavacio:
                    row = rel.copy()
                    row["distribuidora"] = source["nombre"]
                    row["servidor_origen"] = source["base_url"]
                    row["idArticuloPadre"] = art.get("idArticulo")
                    row["fecha_carga"] = fecha_carga
                    row["nro_lote"] = nro_lote
                    rows_relavacio.append(row)

    df_articulos = pd.DataFrame(rows_articulos)
    df_agrupaciones = pd.DataFrame(rows_agrupaciones)
    df_relavacio = pd.DataFrame(rows_relavacio)

    return {
        "articulos": df_articulos,
        "articulos_agrupaciones": df_agrupaciones,
        "articulos_relavacio": df_relavacio,
    }