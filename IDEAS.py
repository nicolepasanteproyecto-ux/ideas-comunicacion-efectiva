# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 08:12:19 2026

@author: practicante-im
"""
import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(page_title="SCAMPER - Experiencia Purdy", page_icon="🎲", layout="centered")

# Inicializar estados
if 'pantalla' not in st.session_state:
    st.session_state.pantalla = 1
if 'letra_elegida' not in st.session_state:
    st.session_state.letra_elegida = ""
if 'pregunta_elegida' not in st.session_state:
    st.session_state.pregunta_elegida = ""

# Base de datos con tus preguntas oficiales
preguntas_scamper = {
    "S - Sustituir": [
        "1. ¿Qué parte del proceso de [área / producto] que hace una persona podríamos cambiar para que lo haga directamente el cliente?",
        "2. ¿Qué hábito o vicio de trabajo antiguo en [área / equipo] podemos cambiar por una regla simple de agilidad?",
        "3. ¿Qué canal tradicional de atención o comunicación en [área] podemos sustituir por una alternativa digital o automatizada?",
        "4. ¿Qué insumo o recurso de un solo uso en [proceso / área] podemos cambiar por una opción reutilizable o digital?",
        "5. ¿Qué métrica tradicional en [área] podemos sustituir por un indicador que realmente mida el valor entregado?",
        "6. ¿Qué trámite o burocracia interna en [área] podemos sustituir por un flujo de aprobación inmediato y transparente?",
        "7. ¿Qué paso del proceso de [área] que genera estrés podemos sustituir por una experiencia guiada y amable?",
        "8. ¿Qué capacitación o instructivo extenso en [área / proceso] podemos sustituir por un formato interactivo o una guía rápida paso a paso?"
    ],
    "C - Combinar": [
        "1. ¿Qué dos pasos o trámites consecutivos en [área / proceso] podemos combinar en una sola acción de un clic?",
        "2. ¿Qué datos o información que hoy pedimos por separado en [proceso] podemos recolectar en un único formulario o punto de contacto?",
        "3. ¿Qué beneficio o incentivo de bienestar podemos combinar con una meta u objetivo de trabajo en [área]?",
        "4. ¿Qué dos indicadores o métricas de [área] podemos combinar para medir el impacto real en una sola mirada?",
        "5. ¿Qué tarea de [área A] podemos combinar con el flujo de [área B] para evitar que el cliente explique su caso dos veces?",
        "6. ¿Qué base de conocimientos estática y chat de consultas frecuentes en [área] podemos integrar en una sola plataforma inteligente?",
        "7. ¿Qué evaluación de desempeño y revisión de clima laboral en [área] podemos combinar en una sola conversación de acompañamiento?",
        "8. ¿Qué reunión de traspaso de proyectos entre [área A] y [área B] podemos combinar con un espacio informal de integración para el equipo?"
    ],
    "A - Adaptar": [
        "1. ¿Qué herramienta o función digital que ya usamos individualmente podemos adaptar como estándar oficial en [área/proceso] para automatizar tareas repetitivas?",
        "2. Adaptemos un estándar externo: Identifiquen un proceso, plantilla o regla ágil que otra área de la empresa o industria ejecute en pocos minutos y adáptalo hoy mismo a [área/proceso].",
        "3. ¿Qué solución aplicada temporalmente durante una emergencia o contingencia operativa podemos adaptar para convertirla en un estándar permanente en [área]?",
        "4. Si adaptamos la lógica de notificaciones automáticas o alertas de una app de uso diario, ¿en qué parte de [proceso] la pondremos para avisar únicamente cuando se requiere intervenir?",
        "5. Para evitar cuellos de botella por firmas o aprobaciones, ¿qué criterio de autorización directa o montos límite de otro proceso exitoso podemos adaptar aquí?",
        "6. ¿Qué experiencia de autogestión o autoservicio de otra plataforma podemos adaptar para que los requerimientos internos se resuelvan sin depender de intermediarios?",
        "7. Desarrollemos un formato de guía visual rápida o lista de verificación (checklist) de un solo paso a paso que permita ejecutar [proceso] sin margen de error ni curvas de aprendizaje largas.",
        "8. Si adaptamos un tablero visual transparente de prioridades (donde todo el equipo ve el estado real de las tareas sin mandar correos), ¿cuáles 3 indicadores clave podríamos ahí?"
    ],
    "M - Modificar": [
        "1. Modifiquemos la escala: Si simplificamos x10 la visibilidad del trabajo de [área], ¿qué tablero o panel deberíamos instalar para que toda la empresa entienda nuestro impacto?",
        "2. Si modificamos la secuencia de [proceso] invirtiendo el orden de los pasos (por ejemplo, validar primero antes de solicitar insumos), ¿qué error o retrabajo evitaríamos?",
        "3. ¿Qué nivel de detalle o precisión innecesaria en los reportes de [proceso] podemos minimizar para enfocarnos solo en los datos que mueven la toma de decisiones?",
        "4. ¿Qué parámetro o criterio de decisión en [proyecto] podemos modificar para que el equipo apruebe o descarte una prueba piloto en menos de 24 horas?",
        "5. Modifiquemos la escala del piloto: Si redujeramos el alcance de [propuesta] a su versión más mínima y rápida de probar (PMV), ¿qué datos reales necesitaríamos para decidir en la mesa si escalarla o descartarla?",
        "6. Si modificamos la asignación de recursos para que el equipo de innovación tenga un 'fondo ciego' o presupuesto preapropado para micro-pilotos de 48 horas, ¿qué tantas pruebas más podríamos ejecutar este mes?",
        "7. Modifiquemos la estructura del pitch: Tomen la presentación de [proyecto / idea] y modifiquen para que dure máximo 3 minutos: 1 minuto para el problema, 1 minuto para la hipótesis de solución y 1 minuto para la decisión exacta que necesita el equipo.",
        "8. ¿Qué parámetro o tolerancia de riesgo en [proyecto / idea] podemos modificar para tomar la decisión de lanzar una prueba piloto con un 70% de certeza en lugar de esperar datos completos?"
    ],
    "P - Proponer otros usos": [
        "1. Si pusiéramos en otro uso el canal de comunicación o retroalimentación que hoy usamos para quejas de clientes, ¿cómo podríamos adaptarlo para capturar ideas rápidas de innovación de los colaboradores?",
        "2. ¿Qué herramienta, recurso o proceso que ya funciona muy bien en otra área de la empresa podemos poner en otro uso para resolver [el reto de hoy] sin inventar nada desde cero?",
        "3. ¿Qué prototipo, idea archivada o proyecto que no se concretó en [área / año pasado] podemos poner en otro uso adaptándolo para resolver el reto de hoy?",
        "4. ¿Qué base de datos de 'ex alumnos', pasantes o ex empleados con los que la empresa mantiene relación en [área] podemos poner en otro uso para pedirles retroalimentación objetiva sobre [la idea]?",
        "5. ¿Qué métrica de rendimiento que el equipo ya revisa en [proceso] podemos poner en otro uso como el indicador para saber si la idea tuvo éxito?",
        "6. ¿Qué hábito o costumbre diaria del equipo en [área] podemos poner en otro uso para asegurar que esta nueva idea se vuelva una rutina natural?",
        "7. ¿Qué acuerdo de nivel de servicio o tiempo máximo de respuesta que ya respetamos en [trámite] podemos poner en otro uso como nuestro compromiso de velocidad para este piloto?",
        "8. ¿Qué evento, feria o actividad grupal que ya se realiza en [área / empresa] podemos poner en otro uso como el escenario para lanzar la prueba de esta idea?"
    ],
    "E - Eliminar": [
        "1. ¿Qué paso, requisito o documento en [área / proceso] podemos eliminar hoy mismo para que la idea principal pase del papel a la prueba piloto sin trabas burocráticas?",
        "2. ¿Qué alternativa o de opción extra en [propuesta] podemos eliminar para dejar solo una ruta clara y tomar la decisión sin dudar?",
        "3. ¿Qué paso del alcance inicial de la idea en [área / proyecto] podemos eliminar temporalmente para tener la primera versión probada esta misma semana?",
        "4. ¿Qué datos, campos o requisitos innecesarios en el formulario o plan de [proceso] podemos eliminar para simplificar la propuesta a su mínima expresión viable?",
        "5. ¿Qué punto de fricción o complicación técnica que frena al usuario en [área] podemos eliminar para que la solución sea simple y directa de implementar?",
        "6. ¿Qué reunión de revisión o comité innecesario podemos eliminar para sustituirlo por una decisión directa del equipo en esta misma sesión?",
        "7. ¿Qué supuesto o duda sobre el usuario en [área] podemos eliminar de la discusión y darlo por válido para tomar hoy la decisión de avanzar?",
        "8. ¿Qué funcionalidad o beneficio secundario en [propuesta] podemos eliminar para enfocar el 100% de los recursos únicamente en el problema principal?"
    ],
    "R - Reorganizar": [
        "1. ¿Qué pasaría si invertimos el orden en [proceso] y entregamos primero la solución o beneficio al usuario antes de pedirle requisitos o formularios?",
        "2. ¿Qué pasó que normalmente dejamos para el final de [proyecto] podemos mover al puro inicio para saber hoy mismo si la idea va a funcionar?",
        "3. ¿Qué pasaría si en lugar de esperar a que el usuario venga con un problema en [proceso], nos adelantamos y le enviamos la solución antes de que la pida?",
        "4. ¿Cómo cambiaría el trabajo en [equipo] si en lugar de buscar la información manualmente, reordenar el sistema para que la información le llegue sola al colaborador?",
        "5. En lugar de hacer las revisiones de [trámite] una por una en fila, ¿cómo podemos reordenarlas para que varias personas las aprueben al mismo tiempo?",
        "6. ¿Qué pasaría si probamos esta idea primero en [área / sucursal] durante una sola semana antes de aplicarla a toda la empresa?",
        "7. ¿Cómo podemos reordenar el orden de las tareas en [proceso] para resolver primero lo que genera más valor y dejar lo secundario para después?",
        "8. ¿Qué pasaría si en lugar de explicar primero todo el proceso en [área], mostramos directamente el resultado final para captar el interés inmediato del usuario?"
    ]
}

ARCHIVO_IDEAS = "respuestas_scamper.csv"

# ==========================================
# PANTALLA 1: CUADRÍCULA DE 2 COLUMNAS EN MÓVIL Y ESCRITORIO
# ==========================================
if st.session_state.pantalla == 1:
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF;
        }
        /* Estilo base de los 7 botones cuadrados */
        div[data-testid="stButton"] button {
            width: 125px !important;
            height: 125px !important;
            border-radius: 16px !important;
            border: none !important;
            box-shadow: none !important;
            transition: transform 0.15s ease !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 8px auto !important;
        }
        div[data-testid="stButton"] button:hover {
            transform: scale(1.04) !important;
            filter: brightness(0.96) !important;
        }
        div[data-testid="stButton"] button p {
            font-size: 52px !important;
            font-weight: 800 !important;
            color: #000000 !important;
            margin: 0 !important;
            line-height: 1 !important;
        }

        /* Mantener las columnas en fila en celular para que no se apilen en 1 sola columna */
        @media (max-width: 768px) {
            div[data-testid="stHorizontalBlock"] {
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                justify-content: center !important;
                align-items: center !important;
                gap: 8px !important;
            }
            div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
                width: auto !important;
                min-width: 0 !important;
                flex: 1 1 0 !important;
            }
            div[data-testid="stButton"] button {
                width: 112px !important;
                height: 112px !important;
                margin: 6px auto !important;
            }
            div[data-testid="stButton"] button p {
                font-size: 44px !important;
            }
        }

        /* Colores exactos según la imagen usando la clase del key de cada botón */
        .st-key-btn_S button { background-color: #DFD862 !important; } /* Amarillo / Ámbar suave */
        .st-key-btn_C button { background-color: #E7AD70 !important; } /* Naranja suave */
        .st-key-btn_A button { background-color: #9EEB6D !important; } /* Verde claro */
        .st-key-btn_M button { background-color: #6B82EA !important; } /* Azul */
        .st-key-btn_P button { background-color: #B46AE8 !important; } /* Morado / Violeta */
        .st-key-btn_E button { background-color: #EB6E60 !important; } /* Rojo / Coral */
        .st-key-btn_R button { background-color: #70C3E4 !important; } /* Turquesa / Cian */
        </style>
    """, unsafe_allow_html=True)

    st.title("🎲 SCAMPER - Experiencia Purdy")
    st.markdown("1. Gira la ruleta y **selecciona la letra** que te tocó:")
    st.write("")

    _, c1, c2, _ = st.columns([0.8, 1, 1, 0.8])
    with c1:
        if st.button("S", key="btn_S"):
            st.session_state.letra_elegida = "S - Sustituir"
            st.session_state.pantalla = 2
            st.rerun()
    with c2:
        if st.button("C", key="btn_C"):
            st.session_state.letra_elegida = "C - Combinar"
            st.session_state.pantalla = 2
            st.rerun()

    _, c3, c4, _ = st.columns([0.8, 1, 1, 0.8])
    with c3:
        if st.button("A", key="btn_A"):
            st.session_state.letra_elegida = "A - Adaptar"
            st.session_state.pantalla = 2
            st.rerun()
    with c4:
        if st.button("M", key="btn_M"):
            st.session_state.letra_elegida = "M - Modificar"
            st.session_state.pantalla = 2
            st.rerun()

    _, c5, c6, _ = st.columns([0.8, 1, 1, 0.8])
    with c5:
        if st.button("P", key="btn_P"):
            st.session_state.letra_elegida = "P - Proponer otros usos"
            st.session_state.pantalla = 2
            st.rerun()
    with c6:
        if st.button("E", key="btn_E"):
            st.session_state.letra_elegida = "E - Eliminar"
            st.session_state.pantalla = 2
            st.rerun()

    _, c7, _ = st.columns([1.3, 1, 1.3])
    with c7:
        if st.button("R", key="btn_R"):
            st.session_state.letra_elegida = "R - Reorganizar"
            st.session_state.pantalla = 2
            st.rerun()

# ==========================================
# PANTALLA 2: 8 Rectángulos Blancos con Borde
# ==========================================
elif st.session_state.pantalla == 2:
    st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF;
        }
        /* Estilo de los rectángulos blancos con borde para las 8 preguntas */
        div[data-testid="stButton"] button {
            width: 100% !important;
            min-height: 75px !important;
            height: auto !important;
            background-color: #FFFFFF !important;
            border: 1.5px solid #CBD5E1 !important;
            border-radius: 6px !important;
            padding: 16px 20px !important;
            margin-bottom: 10px !important;
            box-shadow: none !important;
            transition: all 0.15s ease !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        div[data-testid="stButton"] button:hover {
            border-color: #1E293B !important;
            background-color: #F8FAFC !important;
            transform: translateY(-1px) !important;
        }
        div[data-testid="stButton"] button p {
            font-size: 16px !important;
            font-weight: 500 !important;
            color: #1E293B !important;
            text-align: center !important;
            line-height: 1.4 !important;
            margin: 0 !important;
        }
        /* Estilo distinto para el botón de volver */
        .st-key-btn_volver button {
            min-height: 45px !important;
            border: 1px solid #E2E8F0 !important;
            background-color: #F1F5F9 !important;
            margin-top: 15px !important;
        }
        .st-key-btn_volver button p {
            font-size: 15px !important;
            font-weight: 600 !important;
            color: #475569 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title(f"{st.session_state.letra_elegida}")
    st.markdown("Selecciona la pregunta de tu ruleta:")
    st.write("")

    opciones_preguntas = preguntas_scamper[st.session_state.letra_elegida]

    for idx, pregunta in enumerate(opciones_preguntas):
        if st.button(pregunta, key=f"preg_{idx}", use_container_width=True):
            st.session_state.pregunta_elegida = pregunta
            st.session_state.pantalla = 3
            st.rerun()

    if st.button("⬅️ Volver a Letras", key="btn_volver", use_container_width=True):
        st.session_state.pantalla = 1
        st.rerun()

# ==========================================
# PANTALLA 3: Espacio de Respuesta y Envío con Carro Grande
# ==========================================
elif st.session_state.pantalla == 3:
    st.title("💡 Registro de Idea")
    st.info(f"**Letra:** {st.session_state.letra_elegida}\n\n**Pregunta:** {st.session_state.pregunta_elegida}")
    st.write("Escribe tu solución o idea detallada:")
    idea_usuario = st.text_area("Espacio de respuesta:", placeholder="Escribe aquí tu solución...")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Cambiar pregunta", use_container_width=True):
            st.session_state.pantalla = 2
            st.rerun()
    with c2:
        if st.button("🚀 Enviar mi idea", type="primary", use_container_width=True):
            if idea_usuario.strip() != "":
                nueva_respuesta = {"Letra": [st.session_state.letra_elegida], "Pregunta": [st.session_state.pregunta_elegida], "Idea": [idea_usuario]}
                df_nuevo = pd.DataFrame(nueva_respuesta)
                if os.path.exists(ARCHIVO_IDEAS):
                    df_nuevo.to_csv(ARCHIVO_IDEAS, mode='a', header=False, index=False)
                else:
                    df_nuevo.to_csv(ARCHIVO_IDEAS, mode='w', header=True, index=False)
                
                st.success("¡Idea guardada exitosamente en la base de datos!")
                
                # Animación de carro gigante cruzando la pantalla
                st.markdown("""
                    <style>
                    @keyframes cruzarCarro {
                        0% { left: -250px; opacity: 1; }
                        90% { opacity: 1; }
                        100% { left: 110vw; opacity: 0; }
                    }
                    .carro-animado {
                        position: fixed;
                        bottom: 10%;
                        font-size: 150px;
                        z-index: 9999;
                        pointer-events: none;
                        display: inline-block;
                        transform: scaleX(-1); /* Voltea el emoji para que mire hacia la derecha */
                        animation: cruzarCarro 2.8s ease-in-out forwards;
                    }
                    </style>
                    <div class="carro-animado">🚗💨</div>
                """, unsafe_allow_html=True)

                if st.button("🔄 Registrar otra idea"):
                    st.session_state.pantalla = 1
                    st.rerun()
            else:
                st.warning("Por favor escribe una idea antes de enviar.")