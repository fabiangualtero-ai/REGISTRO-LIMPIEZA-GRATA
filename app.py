import streamlit as st
import pandas as pd
from datetime import datetime, time
import os

# ==========================================
# 1. CONFIGURACIÓN DEL PIN Y DATOS
# ==========================================
# Cambia "1234" por la clave que tú quieras (mantén las comillas)
PIN_ADMIN = "5678" 

# Nombre exacto de tu archivo de imagen que subiste a GitHub
ARCHIVO_LOGO = "Footer_Global.png"

COLABORADORAS = ["Erika", "Marcela"]
INMUEBLES = [
    "Juan Bravo 7", "Tarin", "Emilio", "Baluarte", "Castello 25", 
    "NB40", "AMGC", "Castello 73", "Españoleto 24", "Galileo"
]
ACTIVIDADES = [
    "Planchado", "Limpieza General", "Limpieza Profunda", 
    "Tender Camas", "Organizar Closets", "Compra de Implementos de aseo"
]
ARCHIVO_REGISTROS = "registro_limpieza.csv"

# ==========================================
# 2. CONFIGURACIÓN DE LA PÁGINA (LOGO Y TÍTULO)
# ==========================================
# Configuramos la pestaña del navegador
st.set_page_config(page_title="Gestión de Limpieza", layout="centered")

# MOSTRAR EL LOGO CENTRADO (si existe)
# Truco para centrar: usamos columnas y ponemos la imagen en la central.
if os.path.exists(ARCHIVO_LOGO):
    col1, col2, col3 = st.columns([1,1,1]) # Divide el ancho en 3 partes iguales
    with col2: # Usamos la columna del centro
        # Puedes ajustar el 'width' (ancho) si el logo se ve muy grande o pequeño.
        st.image(ARCHIVO_LOGO, width=180) 

# TÍTULO PRINCIPAL DE LA APP (más profesional, sin emojis)
st.markdown("<h1 style='text-align: center;'>Gestión de Limpieza</h1>", unsafe_allow_html=True)
st.write("---")

# ==========================================
# 3. FORMULARIO PARA ERIKA Y MARCELA
# ==========================================
with st.form("registro_trabajo", clear_on_submit=True):
    st.subheader("Nueva Entrada de Servicio")
    col1, col2 = st.columns(2)
    
    with col1:
        empleada = st.selectbox("Selecciona tu nombre:", COLABORADORAS)
        lugar = st.selectbox("Inmueble / Lugar:", INMUEBLES)
    
    with col2:
        fecha = st.date_input("Fecha:", datetime.now())
        # Selector de horario (de 6:00 a 23:00, cada 30 min)
        h_inicio, h_fin = st.select_slider(
            "Rango de Horario (Inicio - Fin):",
            options=[time(h, m) for h in range(6, 23) for m in (0, 30)],
            value=(time(9, 0), time(12, 0)) # Valores por defecto (9:00 a 12:00)
        )
    
    st.write("---")
    tareas = st.multiselect("Actividades principales realizadas:", ACTIVIDADES)
    lavadas = st.number_input("Número (#) de lavadas realizadas:", min_value=0, step=1, value=0)
    notas = st.text_area("Notas adicionales (opcional):")
    
    # BOTÓN PARA GUARDAR
    boton_guardar = st.form_submit_button("GUARDAR REGISTRO")

# LÓGICA DE ALMACENAMIENTO DE DATOS
if boton_guardar:
    # Calcular horas totales automáticamente
    dt_i = datetime.combine(fecha, h_inicio)
    dt_f = datetime.combine(fecha, h_fin)
    dif = dt_f - dt_i
    total_horas = round(dif.total_seconds() / 3600, 2)
    
    # Crear el nuevo registro
    nuevo_dato = pd.DataFrame([{
        "Fecha": fecha.strftime("%d/%m/%Y"),
        "Nombre": empleada,
        "Inmueble": lugar,
        "Inicio": h_inicio.strftime("%H:%M"),
        "Fin": h_fin.strftime("%H:%M"),
        "Total_Horas": total_horas,
        "Tareas": ", ".join(tareas),
        "Num_Lavadas": lavadas,
        "Comentarios": notas
    }])
    
    # Guardar en el archivo CSV (añadir al final)
    if not os.path.exists(ARCHIVO_REGISTROS):
        nuevo_dato.to_csv(ARCHIVO_REGISTROS, index=False)
    else:
        nuevo_dato.to_csv(ARCHIVO_REGISTROS, mode='a', header=False, index=False)
    
    st.success(f"✅ ¡Registro guardado para {empleada} en {lugar}!")

# ==========================================
# 4. ZONA PRIVADA (ADMINISTRADOR CON PIN)
# ==========================================
st.write("---")
st.subheader("🔐 Acceso Administrador (Filtros y Descarga)")

# Cuadro para escribir el PIN (type="password" oculta los números)
password = st.text_input("Introduce el PIN para ver reportes:", type="password")

if password == PIN_ADMIN:
    st.success("Acceso concedido")
    if os.path.exists(ARCHIVO_REGISTROS):
        df = pd.read_csv(ARCHIVO_REGISTROS)
        
        # Filtros opcionales para facilitar la vista
        st.write("### Filtrar registros:")
        col_f1, col_f2 = st.columns(2)
        filtro_nombre = col_f1.multiselect("Filtrar por nombre:", COLABORADORAS, default=COLABORADORAS)
        filtro_inmueble = col_f2.multiselect("Filtrar por inmueble:", INMUEBLES, default=INMUEBLES)
        
        df_filtrado = df[
            (df['Nombre'].isin(filtro_nombre)) & 
            (df['Inmueble'].isin(filtro_inmueble))
        ]
        
        # Mostrar la tabla de datos
        st.dataframe(df_filtrado, use_container_width=True)
        
        # BOTÓN DE DESCARGA PARA EXCEL (CSV)
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 DESCARGAR ESTA VISTA (CSV para Excel)",
            data=csv,
            file_name=f"reporte_limpieza_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No hay datos registrados todavía.")
elif password != "":
    st.error("PIN incorrecto. Inténtalo de nuevo.")
