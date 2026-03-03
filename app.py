import streamlit as st
import pandas as pd
from datetime import datetime, time
import os

# ==========================================
# 1. CONFIGURACIÓN DEL PIN Y DATOS
# ==========================================
PIN_ADMIN = "1234" 
ARCHIVO_LOGO = "logo.png"
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
# 2. DISEÑO PROFESIONAL (FONDO BLANCO + DETALLES TIERRA)
# ==========================================
st.set_page_config(page_title="Gestión de Limpieza", layout="centered")

# CSS para integrar el logo blanco y mantener estilo tierra
st.markdown("""
    <style>
    /* Fondo Blanco para que el logo se integre perfectamente */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* Títulos en Marrón Tierra Oscuro */
    h1, h2, h3 {
        color: #3E2723 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Estilo de los Botones en color Arcilla/Tierra */
    .stButton>button {
        background-color: #8D6E63 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.6rem 2rem !important;
    }
    
    .stButton>button:hover {
        background-color: #5D4037 !important;
        border: 1px solid #3E2723 !important;
    }

    /* Bordes de los campos en color arena suave */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-color: #E0E0E0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# MOSTRAR EL LOGO (Centrado y sin bordes visibles)
if os.path.exists(ARCHIVO_LOGO):
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(ARCHIVO_LOGO, use_container_width=True)

st.markdown("<h1 style='text-align: center;'>Gestión de Limpieza</h1>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# 3. FORMULARIO DE REGISTRO
# ==========================================
with st.form("registro_trabajo", clear_on_submit=True):
    st.subheader("📝 Registrar Jornada")
    col1, col2 = st.columns(2)
    
    with col1:
        empleada = st.selectbox("Colaboradora:", COLABORADORAS)
        lugar = st.selectbox("Inmueble:", INMUEBLES)
    
    with col2:
        fecha = st.date_input("Fecha del servicio:", datetime.now())
        h_inicio, h_fin = st.select_slider(
            "Rango de Horario:",
            options=[time(h, m) for h in range(6, 23) for m in (0, 30)],
            value=(time(9, 0), time(12, 0))
        )
    
    st.write("---")
    tareas = st.multiselect("Actividades realizadas:", ACTIVIDADES)
    lavadas = st.number_input("Número de lavadas:", min_value=0, step=1, value=0)
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
    
    st.success(f"✅ ¡Registro guardado! Gracias por tu trabajo, {empleada}.")

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
        
        # Vista rápida de los últimos registros
        st.dataframe(df.tail(10), use_container_width=True)
        
        # Botón de descarga
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DESCARGAR HISTORIAL COMPLETO",
            data=csv,
            file_name=f"reporte_limpieza_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("Aún no hay registros en la base de datos.")
elif password != "":
    st.error("PIN incorrecto.")
