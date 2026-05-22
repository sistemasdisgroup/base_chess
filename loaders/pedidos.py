from datetime import datetime
import pandas as pd

from api_client import get


def extract_pedidos(source: dict, fecha: str):
    fecha_carga = datetime.now()

    rows_pedidos = []
    rows_detalle = []

    data = get(
        base_url=source["base_url"],
        endpoint="pedidos/",
        user=source["user"],
        password=source["password"],
        params={
            "fechaPedido": fecha,
            "facturado": "false",
        },
    )

    pedidos = data.get("pedidos", [])

    print(f"Pedidos encontrados: {len(pedidos)}")

    for p in pedidos:
        pedido = p.copy()

        items = pedido.pop("items", [])

        pedido["distribuidora"] = source["nombre"]
        pedido["servidor_origen"] = source["base_url"]
        pedido["fecha_carga"] = fecha_carga

        rows_pedidos.append(pedido)

        for i in items:
            row = i.copy()
            row["distribuidora"] = source["nombre"]
            row["servidor_origen"] = source["base_url"]
            row["fecha_carga"] = fecha_carga
            row["idPedidoPadre"] = p.get("idPedido")

            rows_detalle.append(row)

    df_pedidos = pd.DataFrame(rows_pedidos)
    df_detalle = pd.DataFrame(rows_detalle)

    return {
        "pedidos": df_pedidos,
        "pedidos_detalle": df_detalle,
    }