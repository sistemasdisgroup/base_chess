from datetime import datetime
import pandas as pd

from api_client import get


def extract_jerarquia_mkt(source: dict):
    fecha_carga = datetime.now()

    rows_segmentos = []
    rows_canales = []
    rows_subcanales = []

    data = get(
        base_url=source["base_url"],
        endpoint="jerarquiaMkt/",
        user=source["user"],
        password=source["password"],
        params={}
    )

    segmentos = data.get("SubcanalesMkt", {}).get("SegmentosMkt", [])

    print(f"Segmentos MKT encontrados: {len(segmentos)}")

    for s in segmentos:
        segmento = s.copy()
        canales = segmento.pop("CanalesMkt", [])

        segmento["distribuidora"] = source["nombre"]
        segmento["servidor_origen"] = source["base_url"]
        segmento["fecha_carga"] = fecha_carga
        rows_segmentos.append(segmento)

        for c in canales:
            canal = c.copy()
            subcanales = canal.pop("SubCanalesMkt", [])

            canal["distribuidora"] = source["nombre"]
            canal["servidor_origen"] = source["base_url"]
            canal["fecha_carga"] = fecha_carga
            rows_canales.append(canal)

            for sc in subcanales:
                subcanal = sc.copy()
                subcanal["distribuidora"] = source["nombre"]
                subcanal["servidor_origen"] = source["base_url"]
                subcanal["fecha_carga"] = fecha_carga
                subcanal["idSegmentoMktPadre"] = s.get("idSegmentoMkt")
                subcanal["desSegmentoMktPadre"] = s.get("desSegmentoMkt")
                rows_subcanales.append(subcanal)

    return {
        "mkt_segmentos": pd.DataFrame(rows_segmentos),
        "mkt_canales": pd.DataFrame(rows_canales),
        "mkt_subcanales": pd.DataFrame(rows_subcanales),
    }