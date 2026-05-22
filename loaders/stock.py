from datetime import datetime
import pandas as pd

from api_client import get


def extract_stock(source: dict, fecha_stock: str | None = None, frescura: bool = False):
    fecha_carga = datetime.now()
    rows = []

    depositos = source.get("depositos_stock", [])

    for deposito in depositos:
        print(f"  -> Stock depósito {deposito}")

        params = {
            "idDeposito": deposito,
            "frescura": str(frescura).lower()
        }

        if fecha_stock:
            params["fechaStock"] = fecha_stock

        data = get(
            base_url=source["base_url"],
            endpoint="stock/",
            user=source["user"],
            password=source["password"],
            params=params,
        )

        stock = data.get("dsStockFisicoApi", {}).get("dsStock", [])

        print(f"     registros: {len(stock)}")

        for s in stock:
            row = s.copy()
            row["distribuidora"] = source["nombre"]
            row["servidor_origen"] = source["base_url"]
            row["fecha_carga"] = fecha_carga
            row["idDeposito_consulta"] = deposito
            rows.append(row)

    return {
        "stock": pd.DataFrame(rows)
    }