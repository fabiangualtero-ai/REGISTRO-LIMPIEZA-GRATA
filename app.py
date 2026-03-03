import streamlit as st
import pandas as pd
from datetime import datetime, time
import os

# ==========================================
# 1. CONFIGURACIÓN DEL PIN Y DATOS
# ==========================================
PIN_ADMIN = "1234" 
ARCHIVO_LOGO = "Footer_Global.png" 
ARCHIVO_REGISTROS = "registro_limpieza.csv"

COLABORADORAS = ["Erika", "Marcela"]
INMUEBLES = [
    "Juan Bravo 7", "Tarin", "Emilio", "Baluarte", "Castello 25", 
    "NB40", "AMGC", "Castello 73", "Españoleto 24", "Galileo"
]
ACTIVIDADES = [
    "Planchado", "Limpieza General", "Limpieza Profunda", 
    "Tender Camas", "Organizar Closets", "Compra de Implementos de aseo"
]

# ==========================================
# 2. DISEÑO CON COLORES TIERRA REFORZADOS
# ==========================================
st.set_page_config(page_title="Gestión de Limpieza", layout="centered")

# CSS Reforzado para asegurar que los colores se muestren
st.markdown("""
    <style>
    /* Fondo Blanco */
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    /* Títulos en Marrón Tierra */
    h1, h2, h3, .stSubheader {
        color: #5D4037 !important;
        font-family: 'Segoe UI', sans-serif;
        font-weight: bold;
    }

    /* Botón GUARDAR en color Terracota */
    div.stButton > button {
        background-color: #A1887F !important;
        color: white !important;
        border: 2px solid #8D6E63 !important;
        border-radius: 10px !important;
        width: 100%;
        height: 3em;
        font-size: 18px;
        font-weight: bold;
    }

    /* Cambio de color al pasar el mouse por el botón */
    div.stButton > button:hover {
        background-color: #5D4037 !important;
        color: #F9F7F2 !important;
    }

    /* Color de la franja del slider de horas */
    .stSlider > div > div > div > div {
        background-color: #A1887F !important;
    }
    </style>
    """, unsafe_allow_html=True)

# MOSTRAR EL LOGO
if os.path.exists(ARCHIVO_LOGO):
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(ARCHIVO_LOGO, use_container_width=True)

st.markdown("<h1 style='text-align: center;'>Gestión de Limpieza</h1>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# 3. FORMULARIO CON HORARIO DE 10:00 A 18:00
# ==========================================
with st.form("registro_trabajo", clear_on_submit=True):
    st.subheader("📝 Registrar Jornada")
    col1, col2 = st.columns(2)
    
    with col1:
        empleada = st.selectbox("Colaboradora:", COLABORADORAS)
        lugar = st.selectbox("Inmueble:", INMUEBLES)
    
    with col2:
        fecha = st.date_input("Fecha del servicio:", datetime.now())
        
        # NUEVA FRANJA HORARIA: 10:00 a 18:00
        opciones_horas = [time(h, m) for h in range(10, 18) for m in (0, 30)] + [time(18, 0)]
        h_inicio, h_fin = st.select_slider(
            "Rango de Horario:",
            options=opciones_horas,
            value=(time(10, 0), time(14, 0))
        )
    
    st.write("---")
    tareas = st.multiselect("Actividades realizadas:", ACTIVIDADES)
    
    # Línea de lavadas corregida para evitar errores de sintaxis
    lavadas = st.number_input("Número de lavadas realizadas:", min_value=0, step=1, value=0)
    
    notas = st.text_area("Observaciones adicionales:")
    
    boton_guardar = st.form_submit_button("GUARDAR DATOS")

# LÓGICA DE GUARDADO
if boton_guardar:
    dt_i = datetime.combine(fecha, h_inicio)
    dt_f = datetime.combine(fecha, h_fin)
    total_horas = round((dt_f - dt_i).total_seconds() / 3600, 2)
    
    nuevo_dato = pd.DataFrame([{
        "Fecha": fecha.strftime("%d/%m/%Y"),
        "Nombre": empleada,
        "Inmueble": lugar,
        "Horas": total_horas,
        "Tareas": ", ".join(tareas),
        "Lavadas": lavadas,
        "Notas": notas
    }])
    
    if not os.path.exists(ARCHIVO_REGISTROS):
        nuevo_dato.to_csv(ARCHIVO_REGISTROS, index=False)
    else:
        nuevo_dato.to_csv(ARCHIVO_REGISTROS, mode='a', header=False, index=False)
    
    st.success(f"✅ ¡Registro guardado! Gracias, {empleada}.")

# ==========================================
# 4. ZONA PRIVADA (ADMIN)
# ==========================================
st.write("---")
st.subheader("🔐 Panel de Administración")
password = st.text_input("Introduce el PIN para descargar:", type="password")

if password == PIN_ADMIN:
    st.info("Acceso autorizado")
    if os.path.exists(ARCHIVO_REGISTROS):
        df = pd.read_csv(ARCHIVO_REGISTROS)
        st.dataframe(df.tail(10), use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DESCARGAR HISTORIAL COMPLETO",
            data=csv,
            file_name=f"reporte_limpieza_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
