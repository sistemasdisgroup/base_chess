from datetime import datetime
import pandas as pd

from api_client import get


def extract_lista_precios(source: dict, fecha: str | None = None):
    fecha_carga = datetime.now()
    rows = []

    listas = source.get("listas_precios", [])

    if not listas:
        print(f"[WARN] {source['nombre']}: no tiene listas de precios configuradas")
        return {"lista_precios": pd.DataFrame()}

    for lista in listas:
        print(f"  -> Lista precios {lista}")

        params = {"Lista": str(lista)}

        if fecha:
            params["Fecha"] = fecha

        data = get(
            base_url=source["base_url"],
            endpoint="listaPrecios/",
            user=source["user"],
            password=source["password"],
            params=params,
        )

        precios = data.get("dsListaPreciosApi", {}).get("eListaPrecios", [])

        print(f"     registros: {len(precios)}")

        for p in precios:
            row = p.copy()
            row["distribuidora"] = source["nombre"]
            row["servidor_origen"] = source["base_url"]
            row["fecha_carga"] = fecha_carga
            row["lista_consultada"] = lista
            row["fecha_consulta_precio"] = fecha
            rows.append(row)

    return {
        "lista_precios": pd.DataFrame(rows)
    }