import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración básica
st.title("⏱️ Registro de Limpieza")
usuarios = ["Empleado 1", "Empleado 2"]
archivo = "registro_horarios.csv"

# Selección de empleado
empleado = st.selectbox("Selecciona tu nombre", usuarios)

col1, col2 = st.columns(2)

with col1:
    if st.button("Registrar ENTRADA"):
        nueva_entrada = {
            "Empleado": empleado,
            "Evento": "ENTRADA",
            "Fecha": datetime.now().strftime("%d/%m/%Y"),
            "Hora": datetime.now().strftime("%H:%M:%S")
        }
        df = pd.DataFrame([nueva_entrada])
        df.to_csv(archivo, mode='a', header=not os.path.exists(archivo), index=False)
        st.success(f"Entrada registrada para {empleado}")

with col2:
    if st.button("Registrar SALIDA"):
        nueva_salida = {
            "Empleado": empleado,
            "Evento": "SALIDA",
            "Fecha": datetime.now().strftime("%d/%m/%Y"),
            "Hora": datetime.now().strftime("%H:%M:%S")
        }
        df = pd.DataFrame([nueva_salida])
        df.to_csv(archivo, mode='a', header=not os.path.exists(archivo), index=False)
        st.warning(f"Salida registrada para {empleado}")

# Sección de Administrador (Oculta o al final)
st.divider()
if st.checkbox("Mostrar registros (Admin)"):
    if os.path.exists(archivo):
        datos = pd.read_csv(archivo)
        st.dataframe(datos)
        st.download_button("Descargar Excel (CSV)", datos.to_csv(index=False), "horarios.csv", "text/csv")
    else:
        st.info("Aún no hay registros.")
