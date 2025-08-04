import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from datetime import date
from services.evolution_service import transform_backend_response
import os

API_URL = os.getenv("API_URL", "http://localhost:8080")

def render_portfolio_tab():
    st.header("📈 Visualización del Portafolio")

    # Selección del portafolio
    portafolio_nombre = st.selectbox("Selecciona un portafolio", ["portafolio 1", "portafolio 2"])
    portafolio_id = 1 if portafolio_nombre == "portafolio 1" else 2

    # Selección del rango de fechas
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Fecha de inicio", value=date(2022, 2, 15), key="fecha_inicio")
    with col2:
        fecha_fin = st.date_input("Fecha de fin", value=date(2022, 3, 4), key="fecha_fin")

    if st.button("🔍 Buscar evolución del portafolio", key="buscar_evolucion_btn"):
        try:
            url = f"{API_URL}/api/portafolio/{portafolio_id}/evolution"
            params = {
                "fechaInicio": fecha_inicio.strftime("%Y-%m-%d"),
                "fechaFin": fecha_fin.strftime("%Y-%m-%d")
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                st.success("✅ Evolución obtenida correctamente.")
                data = response.json()
                df = transform_backend_response(data)
                df["fecha"] = pd.to_datetime(df["fecha"])
                # 📊 Gráfico de área: evolución de pesos w_{i,t}
                fig1 = px.area(
                    df,
                    x="fecha",
                    y="peso",
                    color="activo",
                    title="Evolución de pesos w_{i,t}",
                    labels={"peso": "Peso", "activo": "Activo"}
                )
                st.plotly_chart(fig1)
                # 📈 Gráfico de línea: evolución de V_t
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
            else:
                st.error("❌ Error al obtener la evolución del portafolio.")
        except Exception as e:
            st.error(f"❌ Error al conectar con el backend: {e}")
