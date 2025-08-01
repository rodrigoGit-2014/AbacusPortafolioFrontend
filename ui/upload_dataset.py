import streamlit as st
import requests
import threading
import time

def render_upload_tab():
    st.header("📂 Carga del dataset")
    uploaded_file = st.file_uploader("Selecciona el archivo Excel del portafolio", type=["xlsx"], key="uploader_tab0")

    if st.button("Procesar archivo", key="procesar_btn_tab0"):
        if uploaded_file is not None:
            progress = st.progress(0, text="Procesando archivo...")
            response_container = st.empty()

            try:
                # 1. Enviar POST en segundo plano
                def post_request():
                    files = {"file": uploaded_file.getvalue()}
                    response_container.response = requests.post("http://localhost:8080/etl/import-excel", files=files)

                thread = threading.Thread(target=post_request)
                thread.start()

                # 2. Simular progreso mientras espera
                for i in range(20):
                    time.sleep(0.2)
                    progress.progress(int((i + 1) / 20 * 100), text=f"Procesando... {int((i + 1) / 20 * 100)}%")
                    if not thread.is_alive():
                        break

                thread.join()  # asegurarse que termine
                progress.empty()

                # 3. Evaluar respuesta
                response = getattr(response_container, "response", None)
                if response and response.status_code == 200:
                    st.success("✅ Archivo procesado correctamente.")
                else:
                    st.error("❌ Error en el procesamiento del archivo.")
            except Exception as e:
                progress.empty()
                st.error(f"❌ Error al conectar con el backend: {e}")
        else:
            st.warning("Por favor sube un archivo antes de procesar.")
