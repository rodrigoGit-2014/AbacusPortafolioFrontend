import streamlit as st
import pandas as pd
import requests
import json
import plotly.express as px
import os

st.title("Evaluación de evolución del portafolio")

# --------------------------
# 🔹 Función de transformación
# --------------------------

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

# --------------------------
# 🔹 Controles de entrada
# --------------------------

# Selección de portafolio
portafolio_nombre = st.selectbox("Selecciona un portafolio", ["portafolio 1", "portafolio 2"])
portafolio_id = 1 if portafolio_nombre == "portafolio 1" else 2

# Rango de fechas
col1, col2 = st.columns(2)
with col1:
    fecha_inicio = st.date_input("Fecha de inicio")
with col2:
    fecha_fin = st.date_input("Fecha de fin")

# Definir la URL base desde variable de entorno o usar valor por defecto

API_URL = os.getenv("API_URL", "http://localhost:8080")


# Botón para evaluar
if st.button("📈 Evaluar evolución"):
    # Construcción de la URL
    backend_url = f"{API_URL}/api/portafolio/{portafolio_id}/evolution"
    params = {
        "fechaInicio": fecha_inicio.strftime("%Y-%m-%d"),
        "fechaFin": fecha_fin.strftime("%Y-%m-%d")
    }

    try:
        # Llamada a la API del backend
        response = requests.get(backend_url, params=params)
        response.raise_for_status()
        backend_data = response.json()

        # Procesamiento
        df = transform_backend_response(backend_data)
        df["fecha"] = pd.to_datetime(df["fecha"])

        # Gráfico de área de pesos
        fig1 = px.area(
            df,
            x="fecha",
            y="peso",
            color="activo",
            title="Evolución de pesos w_{i,t}",
            labels={"peso": "Peso", "activo": "Activo"}
        )
        st.plotly_chart(fig1)

        # Gráfico de línea de valor total
        df_valor = df.drop_duplicates(subset="fecha")
        fig2 = px.line(
            df_valor,
            x="fecha",
            y="portafolio_total",
            title="Evolución del valor total Vₜ",
            markers=True,
            labels={"portafolio_total": "Vₜ"}
        )
        st.plotly_chart(fig2)

    except requests.exceptions.RequestException as e:
        st.error(f"Error al consultar el backend: {e}")
