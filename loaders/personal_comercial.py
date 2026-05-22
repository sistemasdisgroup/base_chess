from datetime import datetime
import pandas as pd

from api_client import get


def extract_personal_comercial(source: dict):
    fecha_carga = datetime.now()
    rows = []

    data = get(
        base_url=source["base_url"],
        endpoint="personalComercial/",
        user=source["user"],
        password=source["password"],
        params={}  # 👈 sin filtros
    )

    personal = data.get("PersonalComercial", {}).get("ePersCom", [])

    print(f"Personal encontrado: {len(personal)}")

    for p in personal:
        row = p.copy()
        row["distribuidora"] = source["nombre"]
        row["servidor_origen"] = source["base_url"]
        row["fecha_carga"] = fecha_carga
        rows.append(row)

    df = pd.DataFrame(rows)

    return {
        "personal_comercial": df
    }