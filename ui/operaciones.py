# /ui/operaciones.py
import streamlit as st
import requests
import pandas as pd
from datetime import date

def render_operacion_tab():
    st.header("🔄 Operación de Compra/Venta")

    fecha_operacion = st.date_input("Fecha de operación", value=date.today())

    st.subheader("💸 Vendedor")
    col1, col2 = st.columns(2)
    with col1:
        activo_vende = st.selectbox("Activo a vender", ["EEUU","Europa","Japón","EM Asia","Latam","High Yield","IG Corporate","EMHC","Latam HY","UK","Asia Desarrollada","EMEA","Otros RV","Tesoro","MBS+CMBS+AMBS","ABS","MM/Caja"
])
    with col2:
        monto_venta = st.number_input("Monto a vender", min_value=0, step=1000)

    st.subheader("🛒 Comprador")
    col3, col4 = st.columns(2)
    with col3:
        activo_compra = st.selectbox("Activo a comprar", ["EEUU","Europa","Japón","EM Asia","Latam","High Yield","IG Corporate","EMHC","Latam HY","UK","Asia Desarrollada","EMEA","Otros RV","Tesoro","MBS+CMBS+AMBS","ABS","MM/Caja"
])
    with col4:
        monto_compra = st.number_input("Monto a comprar", min_value=0, step=1000)

    if st.button("Ejecutar operación"):
        payload = {
            "day": fecha_operacion.strftime("%Y-%m-%d"),
            "seller": {
                "asset": activo_vende,
                "amount": monto_venta
            },
            "buyer": {
                "asset": activo_compra,
                "amount": monto_compra
            }
        }

        try:
            response = requests.post("http://localhost:8080/api/portfolio/1/operation", json=payload)
            response.raise_for_status()
            result = response.json()

            st.success(f"✅ Operación registrada exitosamente: {activo_vende} → {activo_compra}")

            # Mostrar resultado de la operación
            st.subheader(f"📊 Resultado para el {result['day']}")
            st.metric("Valor total del portafolio", f"${result['portfolioTotal']:,.2f}")
            st.markdown("### 📈 Detalle por activo")

            for asset in result["assetOperations"]:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown("**Activo**")
                    st.markdown(f"{asset['assetName']}")
                with col2:
                    st.markdown("**Precio**")
                    st.markdown(f"${asset['priceAmount']:,.2f}")
                with col3:
                    st.markdown("**Cantidad**")
                    st.markdown(f"{asset['assetAmount']:,.2f}")
                with col4:
                    st.markdown("**Peso**")
                    st.markdown(f"{asset['weight']:.2%}")
                st.markdown("---")
           
           # df = pd.DataFrame(result["assetOperations"])
           # df.columns = ["Activo", "Precio", "Cantidad", "Peso"]
           # st.dataframe(df.style.format({
           #     "Precio": "{:,.2f}",
           #     "Cantidad": "{:,.2f}",
           #     "Peso": "{:.2%}"
           # }))

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error al registrar la operación: {str(e)}")
