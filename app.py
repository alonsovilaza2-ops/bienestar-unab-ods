import streamlit as st
from datetime import datetime
import pandas as pd

#========================================
# CONFIGURACIÓN VISUAL (ESTILO APP)
#========================================
st.set_page_config(page_title="Bienestar UNAB", page_icon="🌱")

# CSS para que se vea más como una App móvil
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #004a99; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌱 Asistente de Bienestar")
st.caption("Proyecto ODS 3 e Ingeniería - UNAB Sede República")

#========================================
# LOGICA DE DATOS
#========================================
# Usamos diccionarios para simular la base de datos nutricional del proyecto
alimentos_db = {
    "Manzana": "Saludable - Aporta vitaminas y fibra.",
    "Avena": "Saludable - Rica en fibra y energía.",
    "Yogurt": "Saludable - Calcio y proteínas.",
    "Pizza": "No Saludable - Exceso de grasas y sodio.",
    "Hamburguesa": "No Saludable - Alta en grasas saturadas."
}

#========================================
# INTERFAZ DE NAVEGACIÓN
#========================================
menu = st.sidebar.selectbox("Ir a:", ["Registro Diario", "Tareas Académicas", "Técnicas de Relajación", "Mi Impacto (ODS)"])

#--- REGISTRO DIARIO ---
if menu == "Registro Diario":
    st.header("¿Cómo va tu día?")
    
    nombre = st.text_input("Nombre del Estudiante")
    emocion = st.select_slider("Estado Emocional:", options=["Cansado", "Ansioso", "Estresado", "Feliz"])
    
    if emocion in ["Ansioso", "Estresado"]:
        st.warning("⚠️ Nota: Recuerda que en Sede República tienes apoyo psicológico gratuito.")
        
    comida = st.selectbox("¿Qué almorzaste/comiste?", list(alimentos_db.keys()) + ["Otro"])
    
    if st.button("Guardar Registro"):
        st.success("Datos guardados en la nube del proyecto.")
        if comida in alimentos_db:
            st.info(f"Análisis Nutricional: {alimentos_db[comida]}")

#--- TAREAS ---
elif menu == "Tareas Académicas":
    st.header("Gestión del Tiempo")
    tarea = st.text_input("Certamen o Entrega")
    fecha = st.date_input("Fecha límite")
    if st.button("Agendar"):
        st.write(f"📌 {tarea} agendada para el {fecha}. ¡Organizarse reduce el estrés!")

#--- RELAJACIÓN ---
elif menu == "Técnicas de Relajación":
    st.header("Pausa Activa")
    tecnica = st.radio("Elige una:", ["Respiración 4-7-8", "Escuchar música Lo-Fi", "Hidratación consciente"])
    if st.button("Comenzar"):
        st.balloons()
        st.info("Iniciando temporizador de 5 minutos...")

#--- ESTADÍSTICAS ---
elif menu == "Mi Impacto (ODS)":
    st.header("Tu contribución al ODS 10")
    st.metric(label="Días de autocuidado", value="12", delta="3 esta semana")
    st.write("Al usar esta app, democratizas el acceso a la salud mental.")
