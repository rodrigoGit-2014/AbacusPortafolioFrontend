import pandas as pd

def transform_backend_response(data):
    registros = []
    for entry in data:
        fecha = entry["day"]
        portafolio_total = round(entry["portfolioTotal"], 2)
        for weight in entry["weights"]:
            registros.append({
                "fecha": fecha,
                "activo": weight["assetName"],
                "peso": round(weight["assetWeight"], 3),
                "portafolio_total": portafolio_total
            })
    return pd.DataFrame(registros)
