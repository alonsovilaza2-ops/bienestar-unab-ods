import streamlit as st
from datetime import datetime
import pandas as pd
import time
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

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
calorias_db = {
    "Manzana": 95,
    "Avena": 150,
    "Yogurt": 120,
    "Pizza": 285,
    "Hamburguesa": 354
}
alimentos_db = {
    "Manzana": "Saludable - Aporta vitaminas y fibra.",
    "Avena": "Saludable - Rica en fibra y energía.",
    "Yogurt": "Saludable - Calcio y proteínas.",
    "Pizza": "No saludable - Exceso de grasas y sodio.",
    "Hamburguesa": "No saludable - Alta en grasas saturadas."
}

#========================================
# INTERFAZ DE NAVEGACIÓN
#========================================
menu = st.sidebar.selectbox(
    "Ir a:",
    [
        "Registro Diario",
        "Tareas Académicas",
        "Técnicas de Relajación",
        "Mi Impacto (ODS)",
        "Asistente Virtual",
        "Donaciones"
    ]
)

#--- REGISTRO DIARIO ---
if menu == "Registro Diario":
    st.header("¿Cómo va tu día?")
    
    nombre = st.text_input("Nombre del Estudiante")
    emocion = st.select_slider("Estado Emocional:", options=["Cansado", "Ansioso", "Estresado", "Feliz"])
    
    if emocion in ["Ansioso", "Estresado"]:
        st.warning("⚠️ Nota: Recuerda que en Sede República tienes apoyo psicológico gratuito.")
        
    comida = st.selectbox(
    "¿Qué almorzaste/comiste?",
    list(alimentos_db.keys()) + ["Otro"]
)

if comida == "Otro":
    comida_personalizada = st.text_input("Escribe el alimento")

    calorias_manual = st.number_input(
        "Calorías aproximadas del alimento",
        min_value=0,
        value=100
    )
    
    
   if st.button("Guardar Registro"):

    st.success("Datos guardados en la nube del proyecto.")

    if comida in alimentos_db:
        st.info(f"Análisis Nutricional: {alimentos_db[comida]}")
        st.write(f"🔥 Calorías aproximadas: {calorias_db[comida]} kcal")

    elif comida == "Otro":
        st.write(f"🍽️ Alimento registrado: {comida_personalizada}")
        st.write(f"🔥 Calorías aproximadas: {calorias_manual} kcal")
    
       
       st.markdown("## ❤️ Ayuda a otros estudiantes")


#--- TAREAS ---
elif menu == "Tareas Académicas":
    st.header("Gestión del Tiempo")
    tarea = st.text_input("Certamen o Entrega")
    fecha = st.date_input("Fecha límite")
    if st.button("Agendar"):
        st.write(f"📌 {tarea} agendada para el {fecha}. ¡Organizarse reduce el estrés!")

#--- RELAJACIÓN ---


elif menu == "Técnicas de Relajación":
    st.header("🧘 Técnicas de Relajación")

    tecnica = st.radio(
        "Elige una:",
        ["Respiración 4-7-8", "Escuchar música Lo-Fi", "Hidratación consciente"]
    )

    if tecnica == "Respiración 4-7-8":
        st.markdown("""
        ### ¿Qué es la respiración 4-7-8?
        
        Esta técnica ayuda a reducir el estrés y la ansiedad.
        
        Pasos:
        - Inhala por la nariz durante 4 segundos.
        - Mantén la respiración durante 7 segundos.
        - Exhala lentamente durante 8 segundos.
        
        Repite el proceso durante 5 minutos.
        """)

    if st.button("Comenzar"):
        progreso = st.progress(0)

        for i in range(300):  # 300 segundos = 5 minutos
            time.sleep(1)
            progreso.progress((i + 1) / 300)

        st.success("✅ ¡Felicitaciones! Completaste los 5 minutos.")
        st.balloons()
#--- ESTADÍSTICAS ---
elif menu == "Mi Impacto (ODS)":

    st.header("🌍 Tu contribución al ODS 10")

    st.metric(
        label="Días de autocuidado",
        value="12",
        delta="3 esta semana"
    )

    st.success(
        "Cada registro que realizas demuestra tu compromiso con tu bienestar."
    )

    st.info(
        "Cuidar tu salud mental y física hoy puede mejorar tu rendimiento académico mañana."
    )

    st.write("""
    ### 🚀 Tu impacto positivo

    ✅ Has dedicado tiempo a tu bienestar.

    ✅ Estás aprendiendo hábitos saludables.

    ✅ Estás desarrollando habilidades para manejar el estrés.

    ✅ Contribuyes a una comunidad universitaria más saludable.

    ✅ Apoyas el cumplimiento de los Objetivos de Desarrollo Sostenible.
    """)

    st.progress(0.75)

    st.write("🏆 ¡Excelente trabajo! Sigue así y alcanza tu meta mensual.")

#--- ASISTENTE VIRTUAL ---
elif menu == "Asistente Virtual":

    st.header("🤖 Asistente de Bienestar IA")

    pregunta = st.text_area(
        "Escribe tu pregunta",
        placeholder="¿Cómo puedo reducir mi estrés antes de un examen?"
    )

    if st.button("Preguntar"):

        with st.spinner("Pensando..."):

            respuesta = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        Eres un asistente de bienestar estudiantil.
                        Ayudas con estrés, ansiedad, alimentación saludable,
                        hábitos de estudio y salud mental.
                        """
                    },
                    {
                        "role": "user",
                        "content": pregunta
                    }
                ]
            )

            st.write(respuesta.choices[0].message.content)

#--- DONACIONES ---
elif menu == "Donaciones":

    st.header("❤️ Apoya nuestro proyecto")

    st.write("""
    Tu aporte nos ayuda a seguir desarrollando herramientas gratuitas
    para mejorar la salud física y mental de estudiantes.
    """)

    st.link_button(
        "💳 Donar con Mercado Pago",
        "https://link.mercadopago.cl/minimarketplace"
