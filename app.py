import streamlit as st
import pandas as pd
from datetime import datetime, time
import os

# 1. CONFIGURACIÓN DEL PIN Y DATOS
# Puedes cambiar el "1234" por la clave que tú quieras
PIN_ADMIN = "1234" 

COLABORADORAS = ["Erika", "Marcela"]
INMUEBLES = [
    "Juan Bravo 7", "Tarin", "Emilio", "Baluarte", "Castello 25", 
    "NB40", "AMGC", "Castello 73", "Españoleto 24", "Galileo"
]
ACTIVIDADES = [
    "Planchado", "Limpieza General", "Limpieza Profunda", 
    "Tender Camas", "Organizar Closets", "Compra de Implementos de aseo"
]
ARCHIVO = "registro_limpieza.csv"

# 2. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Control Limpieza", page_icon="✨")
st.title("✨ Registro de Limpieza")

# 3. FORMULARIO PARA ERIKA Y MARCELA
with st.form("registro_trabajo", clear_on_submit=True):
    st.subheader("📝 Datos del Servicio")
    col1, col2 = st.columns(2)
    
    with col1:
        empleada = st.selectbox("Selecciona tu nombre:", COLABORADORAS)
        lugar = st.selectbox("Inmueble:", INMUEBLES)
    
    with col2:
        fecha = st.date_input("Fecha:", datetime.now())
        h_inicio, h_fin = st.select_slider(
            "Horario (Inicio - Fin):",
            options=[time(h, m) for h in range(6, 23) for m in (0, 30)],
            value=(time(9, 0), time(12, 0))
        )
    
    st.write("---")
    tareas = st.multiselect("Actividades realizadas:", ACTIVIDADES)
    lavadas = st.number_input("Número de lavadas:", min_value=0, step=1)
    notas = st.text_area("Notas adicionales:")
    
    boton_guardar = st.form_submit_button("💾 GUARDAR REGISTRO")

# LÓGICA DE GUARDADO
if boton_guardar:
    dt_i = datetime.combine(fecha, h_inicio)
    dt_f = datetime.combine(fecha, h_fin)
    dif = dt_f - dt_i
    total_horas = round(dif.total_seconds() / 3600, 2)
    
    nuevo_dato = pd.DataFrame([{
        "Fecha": fecha.strftime("%d/%m/%Y"),
        "Nombre": empleada,
        "Inmueble": lugar,
        "Inicio": h_inicio.strftime("%H:%M"),
        "Fin": h_fin.strftime("%H:%M"),
        "Horas": total_horas,
        "Tareas": ", ".join(tareas),
        "Lavadas": lavadas,
        "Comentarios": notas
    }])
    
    if not os.path.exists(ARCHIVO):
        nuevo_dato.to_csv(ARCHIVO, index=False)
    else:
        nuevo_dato.to_csv(ARCHIVO, mode='a', header=False, index=False)
    
    st.success(f"✅ ¡Registro guardado para {empleada}!")

# 4. ZONA PRIVADA (ADMINISTRADOR)
st.write("---")
st.subheader("🔐 Acceso Administrador")

password = st.text_input("Introduce el PIN para ver reportes:", type="password")

if password == PIN_ADMIN:
    st.success("Acceso concedido")
    if os.path.exists(ARCHIVO):
        df = pd.read_csv(ARCHIVO)
        st.dataframe(df)
        
        # Botón de descarga
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DESCARGAR EXCEL (CSV)",
            data=csv,
            file_name=f"reporte_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No hay datos registrados todavía.")
elif password != "":
    st.error("PIN incorrecto")
