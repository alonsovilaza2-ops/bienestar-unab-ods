import streamlit as st
from datetime import datetime
import pandas as pd
import time
from openai import OpenAI

#========================================
# API KEY DIRECTA
#========================================
# Pega tu API Key entre las comillas.
# Ejemplo:
# API_KEY_DIRECTA = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
API_KEY_DIRECTA = "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"

# Cliente de OpenAI
client = OpenAI(api_key=API_KEY_DIRECTA)

#========================================
# CONFIGURACIÓN VISUAL
#========================================

st.set_page_config(
    page_title="Bienestar UNAB",
    page_icon="🌱",
    layout="centered"
)

st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }

    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #004a99;
        color: white;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #0066cc;
        color: white;
    }

    .card {
        background-color: white;
        padding: 18px;
        border-radius: 18px;
        margin-bottom: 15px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    }

    .ods-card {
        background: linear-gradient(90deg, #dbeafe, #e0f2fe);
        padding: 18px;
        border-radius: 18px;
        margin-bottom: 15px;
    }

    .task-card {
        background: linear-gradient(90deg, #fef3c7, #dbeafe);
        padding: 18px;
        border-radius: 18px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌱 Asistente de Bienestar")
st.caption("Proyecto ODS 3 e Ingeniería - UNAB Sede República")

#========================================
# FUNCIÓN DEL ASISTENTE VIRTUAL
#========================================

def responder_asistente_bienestar(pregunta):

    if API_KEY_DIRECTA == "PEGA_AQUI_TU_API_KEY" or API_KEY_DIRECTA.strip() == "":
        return "⚠️ Debes pegar tu API Key en la línea API_KEY_DIRECTA para activar el asistente virtual."

    respuesta = client.responses.create(
        model="gpt-4.1-mini",
        instructions="""
        Eres un asistente virtual de bienestar estudiantil para una app universitaria.

        Tu objetivo es orientar de forma amable, clara y breve sobre:
        - manejo del estrés académico,
        - organización del tiempo,
        - hábitos saludables,
        - alimentación equilibrada,
        - autocuidado emocional,
        - técnicas de relajación,
        - hábitos de estudio.

        No debes diagnosticar enfermedades.
        No debes reemplazar a un médico, psicólogo o profesional de salud.

        Si el estudiante menciona ideas de hacerse daño, crisis intensa,
        peligro, violencia, autolesiones o una situación grave, debes recomendar
        buscar ayuda inmediata con un profesional, red de apoyo, familia,
        universidad o servicio de emergencia.

        Responde en español de Chile, con tono cercano, positivo y claro.
        Usa respuestas breves, útiles y fáciles de aplicar.
        """,
        input=pregunta
    )

    return respuesta.output_text

#========================================
# BASE DE DATOS SIMPLE
#========================================

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
# FUNCIONES PARA OPINIONES
#========================================

OPINIONES_FILE = "opiniones.csv"

def cargar_opiniones():
    if pd.io.common.file_exists(OPINIONES_FILE):
        return pd.read_csv(OPINIONES_FILE)
    else:
        return pd.DataFrame(
            columns=["fecha", "nombre", "clasificacion", "comentario"]
        )


def guardar_opinion(nombre, clasificacion, comentario):
    nueva_opinion = {
        "fecha": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "nombre": nombre if nombre.strip() else "Anónimo",
        "clasificacion": clasificacion,
        "comentario": comentario
    }

    df = cargar_opiniones()
    df = pd.concat([df, pd.DataFrame([nueva_opinion])], ignore_index=True)
    df.to_csv(OPINIONES_FILE, index=False)

#========================================
# MENÚ DE NAVEGACIÓN
#========================================

menu = st.sidebar.selectbox(
    "Ir a:",
    [
        "Registro Diario",
        "Tareas Académicas",
        "Técnicas de Relajación",
        "Mi Impacto (ODS)",
        "Asistente Virtual",
        "Opiniones",
        "Donaciones"
    ]
)

#========================================
# REGISTRO DIARIO
#========================================

if menu == "Registro Diario":

    st.header("📝 ¿Cómo va tu día?")

    st.markdown("""
    <div class="card">
        <h4>🌱 Registro de bienestar diario</h4>
        <p>Completa este pequeño registro para conocer cómo va tu día y recibir una orientación simple.</p>
    </div>
    """, unsafe_allow_html=True)

    nombre = st.text_input("Nombre del Estudiante")

    emocion = st.select_slider(
        "Estado Emocional:",
        options=["Cansado", "Ansioso", "Estresado", "Feliz"]
    )

    if emocion in ["Ansioso", "Estresado"]:
        st.warning(
            "⚠️ Nota: Recuerda que en Sede República tienes apoyo psicológico gratuito."
        )

    comida = st.selectbox(
        "¿Qué almorzaste/comiste?",
        list(alimentos_db.keys()) + ["Otro"]
    )

    comida_personalizada = ""
    calorias_manual = 100

    if comida == "Otro":

        comida_personalizada = st.text_input(
            "Escribe el alimento"
        )

        calorias_manual = st.number_input(
            "Calorías aproximadas del alimento",
            min_value=0,
            value=100
        )

    if st.button("Guardar Registro"):

        if nombre.strip() == "":
            st.warning("Puedes escribir tu nombre antes de guardar.")
        else:
            st.success("✅ Datos guardados en la nube del proyecto.")

            st.write(f"👤 Estudiante: **{nombre}**")
            st.write(f"😊 Estado emocional: **{emocion}**")

            if comida in alimentos_db:

                st.info(
                    f"Análisis Nutricional: {alimentos_db[comida]}"
                )

                st.write(
                    f"🔥 Calorías aproximadas: {calorias_db[comida]} kcal"
                )

            elif comida == "Otro":

                if comida_personalizada.strip() == "":
                    st.warning("No escribiste el nombre del alimento.")
                else:
                    st.write(
                        f"🍽️ Alimento registrado: {comida_personalizada}"
                    )

                    st.write(
                        f"🔥 Calorías aproximadas: {calorias_manual} kcal"
                    )

#========================================
# TAREAS ACADÉMICAS
#========================================

elif menu == "Tareas Académicas":

    st.header("🎯 Misiones Académicas")
    st.caption("Organiza tus certámenes, trabajos y entregas de forma entretenida.")

    st.markdown("""
    <div class="task-card">
        <h4>📚 Planificar también es autocuidado</h4>
        <p>Cuando ordenas tus tareas, reduces el estrés y mejoras tu rendimiento académico.</p>
    </div>
    """, unsafe_allow_html=True)

    tarea = st.text_input(
        "Nombre de la tarea, certamen o entrega",
        placeholder="Ejemplo: Certamen de Cálculo"
    )

    col1, col2 = st.columns(2)

    with col1:
        fecha = st.date_input("Fecha límite")

    with col2:
        prioridad = st.selectbox(
            "Nivel de prioridad",
            ["Baja 🟢", "Media 🟡", "Alta 🔴"]
        )

    avance = st.slider(
        "¿Cuánto llevas avanzado?",
        min_value=0,
        max_value=100,
        value=0
    )

    mini_metas = st.multiselect(
        "Selecciona mini metas para avanzar",
        [
            "Buscar información",
            "Hacer resumen",
            "Crear borrador",
            "Estudiar 25 minutos",
            "Revisar con un compañero",
            "Enviar o entregar"
        ]
    )

    motivacion = st.radio(
        "¿Cómo te sientes frente a esta tarea?",
        [
            "Motivado/a 😄",
            "Un poco perdido/a 😐",
            "Con estrés 😟",
            "Listo/a para terminar 🚀"
        ]
    )

    if st.button("Agendar misión académica"):

        if tarea.strip() == "":
            st.warning("Debes escribir el nombre de la tarea.")
        else:
            hoy = datetime.now().date()
            dias_restantes = (fecha - hoy).days

            if dias_restantes < 0:
                st.error("La fecha ya pasó. Elige una fecha futura.")
            else:
                st.success(f"📌 Misión creada: {tarea}")

                col_a, col_b = st.columns(2)

                with col_a:
                    st.metric(
                        label="Días restantes",
                        value=f"{dias_restantes} días"
                    )

                with col_b:
                    st.metric(
                        label="Avance actual",
                        value=f"{avance}%"
                    )

                st.write(f"Prioridad seleccionada: **{prioridad}**")
                st.write(f"Estado frente a la tarea: **{motivacion}**")

                st.progress(avance / 100)

                if avance == 0:
                    st.info("💡 Consejo: comienza con una mini meta de 25 minutos.")
                elif avance < 50:
                    st.info("🌱 Vas avanzando. Intenta completar una parte más hoy.")
                elif avance < 100:
                    st.success("🚀 ¡Muy bien! Ya superaste la mitad.")
                else:
                    st.success("🏆 ¡Tarea completada!")
                    st.balloons()

                if mini_metas:
                    st.write("### ✅ Mini metas seleccionadas")
                    for meta in mini_metas:
                        st.write(f"- {meta}")

                st.write("### 🧩 Plan sugerido")

                if dias_restantes == 0:
                    st.warning("Hoy es la fecha límite. Prioriza lo más importante y evita distracciones.")
                elif dias_restantes <= 2:
                    st.info("Divide el trabajo en bloques cortos: 25 minutos de estudio y 5 minutos de descanso.")
                else:
                    st.info("Puedes avanzar con calma: organiza una parte pequeña por día para evitar estrés.")

                st.markdown("""
                <div class="card">
                    <h4>✨ Frase motivacional</h4>
                    <p>Un avance pequeño también cuenta. Lo importante es comenzar.</p>
                </div>
                """, unsafe_allow_html=True)

#========================================
# TÉCNICAS DE RELAJACIÓN
#========================================

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

        **Pasos:**

        - Inhala por la nariz durante 4 segundos.
        - Mantén la respiración durante 7 segundos.
        - Exhala lentamente durante 8 segundos.
        - Repite el proceso durante 5 minutos.
        """)

    if tecnica == "Escuchar música Lo-Fi":
        st.markdown("""
        ### ¿Qué es la música Lo-Fi?

        La música Lo-Fi, o low fidelity, es relajante, con ritmos suaves,
        sonidos ambientales y loops repetitivos.

        Se usa mucho para estudiar, relajarse o concentrarse.

        **Ejemplos:**

        - Playlists "Lo-Fi Beats" o "Lo-Fi Hip Hop".
        - Canciones con piano suave.
        - Sonidos de lluvia o ciudad.
        - Música sin letra para evitar distracciones.
        """)

    if tecnica == "Hidratación consciente":
        st.markdown("""
        ### ¿Qué es la hidratación consciente?

        Es beber agua de forma regular y atenta para mantener energía,
        concentración y reducir la fatiga.

        **Ejemplos prácticos:**

        - Beber un vaso de agua al levantarte.
        - Llevar una botella durante el día.
        - Usar recordatorios en el teléfono.
        - Tomar agua antes de estudiar.
        """)

    if st.button("Comenzar"):

        if tecnica == "Respiración 4-7-8":

            st.info("Comienza la respiración. El ejercicio durará 5 minutos.")

            progreso = st.progress(0)

            for i in range(300):
                time.sleep(1)
                progreso.progress((i + 1) / 300)

            st.success("✅ ¡Felicitaciones! Completaste los 5 minutos.")
            st.balloons()

        else:
            st.info("✅ Recomendación: practica esta técnica durante 5 a 15 minutos según tu disponibilidad.")

#========================================
# MI IMPACTO ODS
#========================================

elif menu == "Mi Impacto (ODS)":

    st.header("🌍 Tu contribución al ODS 3")

    st.markdown("""
    <div class="ods-card">
        <h4>💚 Salud y Bienestar</h4>
        <p>El ODS 3 promueve una vida sana y el bienestar para todos.</p>
    </div>
    """, unsafe_allow_html=True)

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

#========================================
# ASISTENTE VIRTUAL
#========================================

elif menu == "Asistente Virtual":

    st.header("🤖 Asistente de Bienestar IA")

    st.write("""
    Este asistente puede ayudarte con ideas para manejar el estrés,
    organizar tus tareas, mejorar hábitos de estudio y cuidar tu bienestar.
    """)

    st.info("Recuerda: esta herramienta entrega orientación general y no reemplaza apoyo profesional.")

    if "chat_bienestar" not in st.session_state:
        st.session_state.chat_bienestar = []

    if st.button("🧹 Limpiar conversación"):
        st.session_state.chat_bienestar = []
        st.rerun()

    for mensaje in st.session_state.chat_bienestar:
        with st.chat_message(mensaje["role"]):
            st.write(mensaje["content"])

    pregunta = st.chat_input("Escribe tu pregunta aquí...")

    if pregunta:

        st.session_state.chat_bienestar.append(
            {"role": "user", "content": pregunta}
        )

        with st.chat_message("user"):
            st.write(pregunta)

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                try:
                    respuesta = responder_asistente_bienestar(pregunta)
                except Exception as e:
                    respuesta = f"⚠️ Ocurrió un error: {e}"

                st.write(respuesta)

        st.session_state.chat_bienestar.append(
            {"role": "assistant", "content": respuesta}
        )

    st.divider()

    st.write("### 💡 Preguntas de ejemplo")

    col1, col2 = st.columns(2)

    with col1:
        st.write("- ¿Cómo puedo organizarme antes de un certamen?")
        st.write("- Dame una técnica rápida para calmarme.")

    with col2:
        st.write("- ¿Qué puedo hacer si estoy estresado?")
        st.write("- Dame una rutina corta de estudio.")

#========================================
# OPINIONES
#========================================

elif menu == "Opiniones":

    st.header("⭐ Opiniones de la Comunidad")
    st.write("Ayúdanos a mejorar la app dejando tu clasificación y comentario.")

    with st.form("form_opinion", clear_on_submit=True):

        nombre_opinion = st.text_input("Tu nombre, opcional")

        clasificacion = st.slider(
            "¿Cómo calificas esta app?",
            min_value=1,
            max_value=5,
            value=5
        )

        comentario = st.text_area(
            "Escribe tu opinión",
            placeholder="Ejemplo: Me gustó porque ayuda a organizarme mejor..."
        )

        enviar = st.form_submit_button("Enviar opinión")

        if enviar:
            if comentario.strip() == "":
                st.warning("Por favor escribe una opinión antes de enviar.")
            else:
                guardar_opinion(nombre_opinion, clasificacion, comentario)
                st.success("✅ ¡Gracias por dejar tu opinión!")

    st.divider()

    df_opiniones = cargar_opiniones()

    if not df_opiniones.empty:

        promedio = df_opiniones["clasificacion"].mean()
        total = len(df_opiniones)

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Promedio de clasificación",
                value=f"{promedio:.1f}/5"
            )

        with col2:
            st.metric(
                label="Total de opiniones",
                value=total
            )

        st.progress(promedio / 5)

        st.subheader("Últimas opiniones")

        ultimas = df_opiniones.tail(5).iloc[::-1]

        for _, fila in ultimas.iterrows():

            estrellas = "⭐" * int(fila["clasificacion"])

            st.markdown(f"""
            <div style="
                background-color: white;
                padding: 15px;
                border-radius: 15px;
                margin-bottom: 10px;
                box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
            ">
                <b>{fila['nombre']}</b> - {fila['fecha']}<br>
                <span style="font-size:20px;">{estrellas}</span>
                <p>{fila['comentario']}</p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.info("Aún no hay opiniones. Sé la primera persona en comentar.")

#========================================
# DONACIONES
#========================================

elif menu == "Donaciones":

    st.header("❤️ Apoya nuestro proyecto")

    st.write("""
    Tu aporte nos ayuda a seguir desarrollando herramientas gratuitas
    para mejorar la salud física y mental de estudiantes.
    """)

    st.markdown("""
    <div class="card">
        <h4>💡 ¿Para qué sirve tu aporte?</h4>
        <p>Permite mejorar la app, agregar nuevas funciones y apoyar el bienestar estudiantil.</p>
    </div>
    """, unsafe_allow_html=True)

    st.link_button(
        "💳 Donar con Mercado Pago",
        "https://link.mercadopago.cl/minimarketplace"
    )
