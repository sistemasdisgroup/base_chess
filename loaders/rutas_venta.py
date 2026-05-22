from datetime import datetime
import pandas as pd

from api_client import get


def extract_rutas_venta(source: dict):
    fecha_carga = datetime.now()

    rows_rutas = []
    rows_clientes = []

    data = get(
        base_url=source["base_url"],
        endpoint="rutasVenta/",
        user=source["user"],
        password=source["password"],
        params={}
    )

    rutas = data.get("RutasVenta", {}).get("eRutasVenta", [])

    print(f"Rutas encontradas: {len(rutas)}")

    for r in rutas:
        ruta = r.copy()
        clientes = ruta.pop("eClientesRutas", [])

        ruta["distribuidora"] = source["nombre"]
        ruta["servidor_origen"] = source["base_url"]
        ruta["fecha_carga"] = fecha_carga

        rows_rutas.append(ruta)

        for c in clientes:
            row = c.copy()
            row["distribuidora"] = source["nombre"]
            row["servidor_origen"] = source["base_url"]
            row["fecha_carga"] = fecha_carga

            row["idSucursalRuta"] = r.get("idSucursal")
            row["idFuerzaVentasRuta"] = r.get("idFuerzaVentas")
            row["idModoAtencionRuta"] = r.get("idModoAtencion")
            row["idRuta"] = r.get("idRuta")
            row["desRuta"] = r.get("desRuta")
            row["fechaDesdeRuta"] = r.get("fechaDesde")
            row["fechaHastaRuta"] = r.get("fechaHasta")
            row["idPersonalRuta"] = r.get("idPersonal")
            row["desPersonalRuta"] = r.get("desPersonal")

            rows_clientes.append(row)

    return {
        "rutas_venta": pd.DataFrame(rows_rutas),
        "rutas_venta_clientes": pd.DataFrame(rows_clientes),
    }