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


def extract_ventas(source: dict, fecha_desde: str, fecha_hasta: str, detallado: bool = False):
    params_base = {
        "fechaDesde": fecha_desde,
        "fechaHasta": fecha_hasta,
        "detallado": str(detallado).lower(),
        "nroLote": 1,
    }

    data_lote_1 = get(
        base_url=source["base_url"],
        endpoint="ventas/",
        user=source["user"],
        password=source["password"],
        params=params_base,
    )

    # 🔴 ACÁ ESTÁ LA CLAVE
    ventas_lote_1 = data_lote_1.get("dsReporteComprobantesApi", {}).get("VentasResumen", [])

    print(f"Distribuidora: {source['nombre']}")
    print(f"Ventas en lote 1: {len(ventas_lote_1)}")

    fecha_carga = datetime.now()
    rows_ventas = []

    # ⚠️ IMPORTANTE:
    # no tenemos texto tipo "1/XX", así que iteramos hasta que no haya más datos
    nro_lote = 1

    while True:
        print(f"  -> Lote ventas {nro_lote}")

        params = {
            "fechaDesde": fecha_desde,
            "fechaHasta": fecha_hasta,
            "detallado": str(detallado).lower(),
            "nroLote": nro_lote,
        }

        data = get(
            base_url=source["base_url"],
            endpoint="ventas/",
            user=source["user"],
            password=source["password"],
            params=params,
        )

        ventas = data.get("dsReporteComprobantesApi", {}).get("VentasResumen", [])

        # 🔴 condición de corte
        if not ventas:
            print(f"  -> Fin en lote {nro_lote}")
            break

        for v in ventas:
            row = v.copy()
            row["distribuidora"] = source["nombre"]
            row["servidor_origen"] = source["base_url"]
            row["fecha_carga"] = fecha_carga
            row["nro_lote"] = nro_lote
            row["fecha_desde_consulta"] = fecha_desde
            row["fecha_hasta_consulta"] = fecha_hasta
            row["detallado_consulta"] = detallado
            rows_ventas.append(row)

        nro_lote += 1

    df_ventas = pd.DataFrame(rows_ventas)

    return {
        "ventas": df_ventas
    }