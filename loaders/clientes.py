from datetime import datetime
import re
import pandas as pd

from api_client import get


def obtener_total_lotes(texto_cant_clientes):
    """
    Ejemplo de texto:
    'Numero de lote obtenido: 1/73. Cantidad de clientes totales: 7292'
    """
    if not texto_cant_clientes:
        return 1

    match = re.search(r"(\d+)\s*/\s*(\d+)", str(texto_cant_clientes))
    if match:
        return int(match.group(2))

    return 1


def extract_clientes(source: dict):
    # Primero consultamos lote 1 para saber cuántos lotes hay
    data_lote_1 = get(
        base_url=source["base_url"],
        endpoint="clientes/",
        user=source["user"],
        password=source["password"],
        params={"nroLote": 1},
    )

    texto_info = data_lote_1.get("cantClientes")
    total_lotes = obtener_total_lotes(texto_info)

    print(f"Distribuidora: {source['nombre']}")
    print(f"Info API: {texto_info}")
    print(f"Total de lotes a recorrer: {total_lotes}")

    fecha_carga = datetime.now()

    rows_clientes = []
    rows_alias = []
    rows_fuerza = []

    for nro_lote in range(1, total_lotes + 1):
        print(f"  -> Procesando lote {nro_lote}/{total_lotes}")

        data = get(
            base_url=source["base_url"],
            endpoint="clientes/",
            user=source["user"],
            password=source["password"],
            params={"nroLote": nro_lote},
        )

        clientes = data.get("Clientes", {}).get("eClientes", [])

        for c in clientes:
            cliente = c.copy()
            aliases = cliente.pop("eClialias", [])
            fuerzas = cliente.pop("eClifuerza", [])

            cliente["distribuidora"] = source["nombre"]
            cliente["servidor_origen"] = source["base_url"]
            cliente["fecha_carga"] = fecha_carga
            cliente["nro_lote"] = nro_lote
            rows_clientes.append(cliente)

            for a in aliases:
                row = a.copy()
                row["distribuidora"] = source["nombre"]
                row["servidor_origen"] = source["base_url"]
                row["idClientePadre"] = c.get("idCliente")
                row["idSucursalPadre"] = c.get("idSucursal")
                row["fecha_carga"] = fecha_carga
                row["nro_lote"] = nro_lote
                rows_alias.append(row)

            for f in fuerzas:
                row = f.copy()
                row["distribuidora"] = source["nombre"]
                row["servidor_origen"] = source["base_url"]
                row["idClientePadre"] = c.get("idCliente")
                row["idSucursalPadre"] = c.get("idSucursal")
                row["fecha_carga"] = fecha_carga
                row["nro_lote"] = nro_lote
                rows_fuerza.append(row)

    df_clientes = pd.DataFrame(rows_clientes)
    df_alias = pd.DataFrame(rows_alias)
    df_fuerza = pd.DataFrame(rows_fuerza)

    return {
        "clientes": df_clientes,
        "clientes_alias": df_alias,
        "clientes_fuerza": df_fuerza,
    }