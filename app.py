import streamlit as st
from datetime import date
from ui.upload_dataset import render_upload_tab
from ui.visualizacion import render_portfolio_tab

st.set_page_config(page_title="Gestión de Portafolio", layout="wide")
st.title("Gestión de Portafolio Financiero")

tabs = st.tabs(["📂 Carga Dataset", "📊 Visualización Portafolio", "🔄 Operación Compra/Venta"])

# TAB 1: Carga Dataset
with tabs[0]:
    render_upload_tab()
    #st.header("📂 Carga del dataset")
# TAB 2: Visualización Portafolio
with tabs[1]:
    render_portfolio_tab()
    #st.header("📊 Visualización del portafolio")
    #
    #col1, col2, col3 = st.columns(3)
    #with col1:
    #    portafolio_id = st.selectbox("Selecciona el portafolio", [1, 2])
    #with col2:
    #    fecha_inicio = st.date_input("Fecha inicio", value=date(2022, 2, 15))
    #with col3:
    #    fecha_fin = st.date_input("Fecha fin", value=date(2022, 3, 15))
    #
    #if st.button("Buscar evolución del portafolio"):
    #    st.info(f"Consultando portafolio {portafolio_id} desde {fecha_inicio} hasta {fecha_fin}")
    #    # Aquí se consultará la API y se mostrarán gráficos

# TAB 3: Operación Compra/Venta
with tabs[2]:
    st.header("🔄 Operación de Compra/Venta")
    
    fecha_operacion = st.date_input("Fecha de operación", value=date.today())

    st.subheader("💸 Vendedor")
    col1, col2 = st.columns(2)
    with col1:
        activo_vende = st.selectbox("Activo a vender", ["EEUU", "Europa", "Japon"])
    with col2:
        monto_venta = st.number_input("Monto a vender", min_value=0.0, step=1000.0)

    st.subheader("🛒 Comprador")
    col3, col4 = st.columns(2)
    with col3:
        activo_compra = st.selectbox("Activo a comprar", ["EEUU", "Europa", "Japon"])
    with col4:
        monto_compra = st.number_input("Monto a comprar", min_value=0.0, step=1000.0)

    if st.button("Ejecutar operación"):
        st.success(f"Operación registrada: {activo_vende} → {activo_compra}")
        # Aquí se llamará al backend para guardar la operación
