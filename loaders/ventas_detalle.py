from datetime import datetime
import pandas as pd

from api_client import get


def extract_ventas_detalle(source: dict, fecha_desde: str, fecha_hasta: str):
    fecha_carga = datetime.now()
    rows = []

    nro_lote = 1

    while True:
        print(f"  -> Lote ventas detalle {nro_lote}")

        data = get(
            base_url=source["base_url"],
            endpoint="ventas/",
            user=source["user"],
            password=source["password"],
            params={
                "fechaDesde": fecha_desde,
                "fechaHasta": fecha_hasta,
                "detallado": "true",
                "nroLote": nro_lote,
            },
        )

        # 🔴 CORRECTO
        detalle = data.get("dsReporteComprobantesApi", {}).get("VentasResumen", [])

        if not detalle:
            print(f"  -> Fin ventas detalle en lote {nro_lote}")
            break

        for d in detalle:
            row = d.copy()
            row["distribuidora"] = source["nombre"]
            row["servidor_origen"] = source["base_url"]
            row["fecha_carga"] = fecha_carga
            row["nro_lote"] = nro_lote
            row["fecha_desde_consulta"] = fecha_desde
            row["fecha_hasta_consulta"] = fecha_hasta
            rows.append(row)

        nro_lote += 1

    df = pd.DataFrame(rows)

    return {
        "ventas_detalle": df
    }