
# -*- coding: utf-8 -*-
"""
Ruleta SCAMPER - Comunicación de Equipo
"""

import csv
import io
import math
import random
import time
import urllib.parse
import urllib.request

import qrcode
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components


# ==============================================================================
# CONFIGURACIÓN DE ENLACES (APPS SCRIPT QR Y GOOGLE SHEETS)
# ==============================================================================

URL_QR = (
    "https://script.google.com/macros/s/"
    "AKfycby4nMK6bqOTWUGv0hrxAW4njgaJ5vLWrzHRN1JMlUZad51hKTkzXAh2SvSgQJfDItwcpA/exec"
)

SHEET_ID = "1rRngtD0iPbaGrwSXjmR7cfIoBjzwtBLxGgj8CH1PESk"
SHEET_NAME = "Respuestas"


# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==============================================================================

st.set_page_config(
    page_title="Ruleta SCAMPER - Comunicación de Equipo",
    page_icon="🎯",
    layout="wide",
)

st.markdown(
    """
<style>
.stApp {
    background-color: #f8f9fa;
}
.block-container {
    padding-top: 4.5rem;
    padding-bottom: 1rem;
    max-width: 1380px;
}
[data-testid="stTabs"] {
    padding-top: 0.5rem;
}
.titulo-scamper {
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #212529;
    letter-spacing: 3px;
    margin-bottom: 0px;
    line-height: 1.1;
}
.subtitulo-estado {
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    font-weight: 500;
    color: #6c757d;
    margin-bottom: 4px;
}
.barra-vidas {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 6px;
    margin: 4px 0 10px 0;
}
.chip-vida {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 20px;
    padding: 3px 10px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12.5px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 5px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.panel-dimensiones {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 12px;
    padding: 14px 12px;
}
.item-dimension {
    background-color: #f8f9fa;
    border-left: 4px solid #C44B56;
    border-radius: 8px;
    padding: 9px 11px;
    margin-bottom: 8px;
    font-family: 'Segoe UI', sans-serif;
}
.titulo-dimension {
    font-size: 13px;
    font-weight: 700;
    color: #212529;
    margin-bottom: 2px;
}
.detalle-dimension {
    font-size: 12px;
    color: #6c757d;
    line-height: 1.3;
}
.titulo-historial {
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #343a40;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}
.item-historial {
    background-color: #f1f3f5;
    color: #212529;
    padding: 7px 10px;
    margin-bottom: 6px;
    border-radius: 8px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
    font-weight: 700;
}
.nube-contenedor {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    gap: 14px;
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 16px;
    padding: 28px 24px;
    min-height: 320px;
}
.burbuja-nube {
    background-color: #f8f9fa;
    border: 2px solid #dee2e6;
    border-radius: 999px;
    padding: 10px 20px;
    font-family: 'Segoe UI', sans-serif;
    color: #212529;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
div.stButton > button {
    border-radius: 10px;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 700;
    font-size: 14.5px;
    padding: 10px 16px;
    border: none;
}
div.stButton > button[kind="primary"] {
    background-color: #C44B56;
    color: white;
}
div.stButton > button[kind="primary"]:hover {
    background-color: #a83c46;
}
div.stButton > button[kind="secondary"] {
    background-color: #e9ecef;
    color: #495057;
}
div.stButton > button[kind="secondary"]:hover {
    background-color: #dee2e6;
}
</style>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# 2. 4 DIMENSIONES DE REFERENCIA
# ==============================================================================

DIMENSIONES_SESION = [
    {
        "titulo": "1. Compañerismo",
        "detalle": "Cercanía, confianza y conocernos más allá del día a día",
    },
    {
        "titulo": "2. Colaboración",
        "detalle": "Apoyarnos mutuamente y sumar fortalezas entre áreas",
    },
    {
        "titulo": "3. Trabajo en equipo",
        "detalle": "Sentirnos un solo grupo y saber en qué anda cada quien",
    },
    {
        "titulo": "4. Comunicación",
        "detalle": "Conversaciones abiertas, claras y a tiempo entre todos",
    },
]


# ==============================================================================
# 3. DATOS SCAMPER (49 PREGUNTAS: 7 POR CATEGORÍA)
# ==============================================================================

DATOS_SCAMPER = [
    {
        "letra": "S",
        "nombre": "SUSTITUIR",
        "color": "#C44B56",
        "tiempo_inicial": 90,
        "max_salidas": 3,
        "preguntas": [
            "¿Qué forma de comunicarnos podríamos cambiar por una más cercana y sencilla?",
            "¿Qué mensaje podríamos compartir de otra manera para evitar reuniones innecesarias?",
            "¿Qué hábito de comunicación deberíamos dejar atrás para entendernos mejor?",
            "¿Qué canal sería más práctico para compartir las novedades del equipo?",
            "¿Cómo podríamos hacer que pedir ayuda o solicitar algo sea más fácil y directo?",
            "¿Qué forma de dar seguimiento podríamos reemplazar por una que nos ahorre tiempo?",
            "¿Qué palabras o expresiones podríamos utilizar para evitar malentendidos?"
        ],
    },
    {
        "letra": "C",
        "nombre": "COMBINAR",
        "color": "#F2897B",
        "tiempo_inicial": 90,
        "max_salidas": 3,
        "preguntas": [
            "¿Qué momentos de nuestra jornada podríamos aprovechar para conversar más como equipo?",
            "¿Cómo podríamos unir espacios de trabajo para compartir conocimientos y experiencias?",
            "¿Qué temas podríamos mezclar en nuestras conversaciones para conocernos más allá del trabajo?",
            "¿Qué ideas de diferentes compañeros podríamos unir para encontrar mejores soluciones?",
            "¿Qué dinámicas podríamos combinar para que nuestras reuniones sean más participativas?",
            "¿Cómo podríamos conectar los diferentes canales de comunicación para mantenernos mejor informados?",
            "¿Qué intereses en común podríamos aprovechar para generar conversaciones entre compañeros?"
        ],
    },
    {
        "letra": "A",
        "nombre": "ADAPTAR",
        "color": "#F3A155",
        "tiempo_inicial": 90,
        "max_salidas": 3,
        "preguntas": [
            "¿Cómo podríamos explicar nuestras ideas de una manera que todos podamos entender?",
            "¿Qué podríamos aprender de otros equipos para mejorar nuestra comunicación?",
            "¿Cómo podemos adaptar nuestra comunicación cuando tenemos días más cargados de trabajo?",
            "¿Qué información deberíamos compartir desde el inicio para evitar confusiones?",
            "¿Cómo podríamos adaptar nuestros mensajes según la persona o el equipo al que nos dirigimos?",
            "¿Qué buena práctica de comunicación podríamos incorporar a nuestra rutina?",
            "¿Cómo podríamos crear un ambiente donde todos se sientan cómodos compartiendo sus ideas?"
        ],
    },
    {
        "letra": "M",
        "nombre": "MODIFICAR",
        "color": "#F5D687",
        "tiempo_inicial": 90,
        "max_salidas": 3,
        "preguntas": [
            "¿Qué cambiaríamos en nuestras reuniones para que todos tengan más oportunidad de participar?",
            "¿Cómo podríamos mejorar la manera en que compartimos nuestras dudas o inquietudes?",
            "¿Qué podríamos ajustar al momento de ponernos de acuerdo para evitar confusiones?",
            "¿Cómo podríamos cerrar nuestras conversaciones para asegurarnos de que todos entendimos lo mismo?",
            "¿Qué haría que nuestras conversaciones fueran más abiertas y participativas?",
            "¿Cómo podríamos hacer que compartir avances sea más sencillo y visual?",
            "¿Qué pequeño cambio ayudaría a que nuestras conversaciones sean más ágiles y productivas?"
        ],
    },
    {
        "letra": "P",
        "nombre": "PONER EN OTROS USOS",
        "color": "#6C7F54",
        "tiempo_inicial": 90,
        "max_salidas": 3,
        "preguntas": [
            "¿Cómo podríamos aprovechar las reuniones que ya tenemos para fortalecer la relación entre compañeros?",
            "¿Qué otros usos podríamos darles a los espacios que compartimos durante la jornada?",
            "¿Cómo podríamos aprovechar las habilidades de cada compañero para aprender unos de otros?",
            "¿Qué actividad diferente podríamos realizar en nuestros espacios habituales de conversación?",
            "¿Cómo podríamos utilizar los momentos libres para compartir experiencias o inquietudes?",
            "¿De qué otra manera podríamos aprovechar las notas y acuerdos para mantenernos conectados?",
            "¿Cómo podríamos convertir las conversaciones cotidianas en oportunidades para compartir nuevas ideas?"
        ],
    },
    {
        "letra": "E",
        "nombre": "ELIMINAR",
        "color": "#B3CFC3",
        "tiempo_inicial": 90,
        "max_salidas": 3,
        "preguntas": [
            "¿Qué paso podríamos eliminar para que compartir información sea más sencillo?",
            "¿Qué distracciones deberíamos evitar cuando estamos conversando?",
            "¿Qué proceso innecesario nos hace perder tiempo al comunicarnos?",
            "¿Qué costumbre de comunicación ya no nos aporta y deberíamos dejar atrás?",
            "¿Qué información repetitiva podríamos eliminar de nuestros mensajes?",
            "¿Qué barreras nos impiden expresar nuestras opiniones con confianza?",
            "¿Qué situaciones hacen que nuestras conversaciones se alarguen sin llegar a acuerdos?"
        ],
    },
    {
        "letra": "R",
        "nombre": "REORDENAR",
        "color": "#A392AF",
        "tiempo_inicial": 90,
        "max_salidas": 3,
        "preguntas": [
            "¿Qué deberíamos conversar primero para que nuestros intercambios sean más claros?",
            "¿Cómo podríamos organizar la información para que todos encontremos lo que necesitamos?",
            "¿En qué momento de la jornada sería mejor compartir las novedades del equipo?",
            "¿Cómo podríamos distribuir los espacios de participación para escuchar diferentes opiniones?",
            "¿Qué información deberíamos conocer antes de iniciar una conversación importante?",
            "¿Cómo podríamos ordenar nuestras ideas antes de tomar una decisión en equipo?",
            "¿Qué conversaciones podríamos trasladar a otro momento para que todos puedan participar mejor?"
        ],
    },
]

COLORES_LETRA = {item["letra"]: item["color"] for item in DATOS_SCAMPER}


# ==============================================================================
# 4. INICIALIZAR ESTADOS, QR Y LECTURA DE IDEAS
# ==============================================================================

def inicializar_estado():

    if "opciones" not in st.session_state:
        st.session_state.opciones = [
            {**item, "salidas_actuales": 0} for item in DATOS_SCAMPER
        ]

    if "historial" not in st.session_state:
        st.session_state.historial = []

    if "angulo_actual" not in st.session_state:
        st.session_state.angulo_actual = 0

    if "estado_texto" not in st.session_state:
        st.session_state.estado_texto = "Opciones activas: 7 (máx. 3 salidas c/u)"

    if "mostrar_dialogo" not in st.session_state:
        st.session_state.mostrar_dialogo = False

    if "ganador_actual" not in st.session_state:
        st.session_state.ganador_actual = None

    if "pregunta_actual" not in st.session_state:
        st.session_state.pregunta_actual = ""

    if "tiempo_restante" not in st.session_state:
        st.session_state.tiempo_restante = 90

    if "cronometro_activo" not in st.session_state:
        st.session_state.cronometro_activo = False

    if "sonar_campana" not in st.session_state:
        st.session_state.sonar_campana = False

    if "url_qr" not in st.session_state:
        st.session_state.url_qr = URL_QR

    if "refresco_nube" not in st.session_state:
        st.session_state.refresco_nube = 0

    # --------------------------------------------------------------------------
    # ACTUALIZAR PREGUNTAS SIN PERDER LAS SALIDAS REGISTRADAS
    # --------------------------------------------------------------------------

    VERSION_PREGUNTAS = 3

    if st.session_state.get("version_preguntas") != VERSION_PREGUNTAS:

        opciones_anteriores = {
            opcion["letra"]: opcion
            for opcion in st.session_state.opciones
        }

        opciones_actualizadas = []

        for item in DATOS_SCAMPER:
            anterior = opciones_anteriores.get(item["letra"], {})

            opcion_actualizada = {
                **item,
                "salidas_actuales": anterior.get("salidas_actuales", 0)
            }

            opciones_actualizadas.append(opcion_actualizada)

        st.session_state.opciones = opciones_actualizadas

        # Actualizar también el reto si había uno abierto
        if st.session_state.ganador_actual:

            letra_ganadora = st.session_state.ganador_actual["letra"]

            nuevo_ganador = next(
                (
                    opcion for opcion in st.session_state.opciones
                    if opcion["letra"] == letra_ganadora
                ),
                None
            )

            st.session_state.ganador_actual = nuevo_ganador

            if nuevo_ganador:
                if st.session_state.pregunta_actual not in nuevo_ganador["preguntas"]:
                    st.session_state.pregunta_actual = random.choice(
                        nuevo_ganador["preguntas"]
                    )

        st.session_state.version_preguntas = VERSION_PREGUNTAS


@st.cache_data
def crear_imagen_qr(url: str) -> bytes:

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=7,
        border=2,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img: Image.Image = qr.make_image(
        fill_color="#212529",
        back_color="white"
    ).convert("RGB")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    return buffer.getvalue()


def leer_ideas_sheet(nonce: int = 0):

    url_csv = (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq"
        f"?tqx=out:csv&sheet={urllib.parse.quote(SHEET_NAME)}&cachebust={nonce}"
    )

    try:

        req = urllib.request.Request(
            url_csv,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            contenido = resp.read().decode("utf-8", errors="replace")

        if contenido.lstrip().startswith("<!DOCTYPE html") or "<html" in contenido[:200].lower():
            return [], "No se pudo leer el CSV (revisa que el Google Sheet esté compartido como lector)."

        lector = csv.reader(io.StringIO(contenido))
        filas = list(lector)

        if len(filas) <= 1:
            return [], None

        agrupadas = {}

        for fila in filas[1:]:

            letra = fila[1].strip() if len(fila) > 1 else ""
            idea = fila[3].strip() if len(fila) > 3 else ""

            if not idea:
                continue

            clave = idea.lower()

            if clave not in agrupadas:

                agrupadas[clave] = {
                    "idea": idea,
                    "letra": letra[:1].upper() if letra else "",
                    "cantidad": 1,
                }

            else:
                agrupadas[clave]["cantidad"] += 1

        lista = sorted(
            agrupadas.values(),
            key=lambda x: x["cantidad"],
            reverse=True
        )

        return lista, None

    except Exception as e:
        return [], str(e)


inicializar_estado()


# ==============================================================================
# 5. SONIDO DE CAMPANA
# ==============================================================================

def reproducir_campana():

    components.html(
        """
        <script>
        (function() {
            try {
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                const ctx = new AudioCtx();
                const ahora = ctx.currentTime;

                function tocarNota(freq, inicio, duracion) {
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();

                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(freq, inicio);

                    gain.gain.setValueAtTime(0.35, inicio);
                    gain.gain.exponentialRampToValueAtTime(
                        0.001,
                        inicio + duracion
                    );

                    osc.connect(gain);
                    gain.connect(ctx.destination);

                    osc.start(inicio);
                    osc.stop(inicio + duracion);
                }

                tocarNota(880, ahora, 0.9);
                tocarNota(1318.5, ahora + 0.18, 1.1);

            } catch (e) {}
        })();
        </script>
        """,
        height=0,
        width=0,
    )


# ==============================================================================
# 6. DIBUJO DE LA RULETA
# ==============================================================================

def generar_svg_ruleta(opciones, angulo_actual):

    size = 350
    cx = size / 2
    cy = size / 2
    r = 148
    num = len(opciones)

    if num == 0:

        return (
            f'<div style="display:flex;justify-content:center;'
            f'align-items:center;margin:4px 0;">'
            f'<svg width="{size}" height="{size}" '
            f'viewBox="0 0 {size} {size}">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" '
            f'fill="#f8f9fa" stroke="#dee2e6" stroke-width="3"/>'
            f'<text x="{cx}" y="{cy}" fill="#495057" '
            f'font-family="Segoe UI, sans-serif" '
            f'font-size="20" font-weight="bold" '
            f'text-anchor="middle" dominant-baseline="middle">'
            f'¡CICLO COMPLETADO!</text></svg></div>'
        )

    paso = 360.0 / num
    partes = []

    for i, opt in enumerate(opciones):

        start_deg = (angulo_actual + i * paso) % 360
        end_deg = start_deg + paso

        start_rad = math.radians(start_deg - 90)
        end_rad = math.radians(end_deg - 90)

        x1 = cx + r * math.cos(start_rad)
        y1 = cy + r * math.sin(start_rad)

        x2 = cx + r * math.cos(end_rad)
        y2 = cy + r * math.sin(end_rad)

        large_arc = 1 if paso > 180 else 0

        if num == 1:

            partes.append(
                f'<circle cx="{cx}" cy="{cy}" r="{r}" '
                f'fill="{opt["color"]}" stroke="white" '
                f'stroke-width="3"/>'
            )

        else:

            d = (
                f"M {cx},{cy} L {x1:.2f},{y1:.2f} "
                f"A {r},{r} 0 {large_arc},1 "
                f"{x2:.2f},{y2:.2f} Z"
            )

            partes.append(
                f'<path d="{d}" fill="{opt["color"]}" '
                f'stroke="white" stroke-width="3"/>'
            )

        mid_deg = start_deg + (paso / 2.0)
        rot_texto = mid_deg - 90
        mid_rad = math.radians(rot_texto)

        tx = cx + (r * 0.56) * math.cos(mid_rad)
        ty = cy + (r * 0.56) * math.sin(mid_rad)

        font_size = 9 if len(opt["nombre"]) > 14 else 10.5

        color_texto = (
            "#212529"
            if opt["color"] in ["#F5D687", "#B3CFC3"]
            else "#ffffff"
        )

        partes.append(
            f'<text x="{tx:.2f}" y="{ty:.2f}" '
            f'fill="{color_texto}" '
            f'font-family="Segoe UI, sans-serif" '
            f'font-size="{font_size}" font-weight="bold" '
            f'text-anchor="middle" dominant-baseline="middle" '
            f'transform="rotate({rot_texto:.2f}, {tx:.2f}, {ty:.2f})">'
            f'{opt["nombre"]}</text>'
        )

    centro_y_flecha = (
        f'<circle cx="{cx}" cy="{cy}" r="{r * 0.16:.1f}" '
        f'fill="#ffffff" stroke="#c8c8c8" stroke-width="3"/>'
        f'<polygon points="{cx},{cy - r - 13} '
        f'{cx - 11},{cy - r + 4} '
        f'{cx + 11},{cy - r + 4}" fill="#212529"/>'
    )

    return (
        f'<div style="display:flex;justify-content:center;'
        f'align-items:center;margin:0 0 4px 0;">'
        f'<svg width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}">'
        f'{"".join(partes)}{centro_y_flecha}'
        f"</svg></div>"
    )


# ==============================================================================
# 7. BARRA DE VIDAS
# ==============================================================================

def generar_barra_vidas(todas_opciones):

    chips = []

    for opt in todas_opciones:

        restantes = opt["max_salidas"] - opt["salidas_actuales"]

        puntos = (
            "● " * restantes
            + "○ " * opt["salidas_actuales"]
        ).strip()

        opacidad = "1" if restantes > 0 else "0.45"
        color_letra = opt["color"] if restantes > 0 else "#6c757d"

        chips.append(
            f'<div class="chip-vida" style="opacity:{opacidad};">'
            f'<span style="color:{color_letra};'
            f'font-size:14px;font-weight:900;">'
            f'{opt["letra"]}</span>'
            f'<span style="color:{color_letra};'
            f'letter-spacing:1px;">{puntos}</span>'
            f"</div>"
        )

    return f'<div class="barra-vidas">{"".join(chips)}</div>'


# ==============================================================================
# 8. VENTANA EMERGENTE DEL RETO
# ==============================================================================

@st.dialog("Reto SCAMPER", width="small")
def dialogo_reto():

    ganador = st.session_state.ganador_actual

    if not ganador:
        return

    if st.session_state.sonar_campana:

        reproducir_campana()
        st.session_state.sonar_campana = False

    st.markdown(
        f'<div style="text-align:center;'
        f'font-family:Segoe UI,sans-serif;'
        f'font-size:44px;font-weight:800;'
        f'color:{ganador["color"]};line-height:1.1;'
        f'text-shadow:1px 1px 2px rgba(0,0,0,0.08);">'
        f'{ganador["letra"]} - {ganador["nombre"]}</div>'
        f'<div style="text-align:center;'
        f'font-family:Segoe UI,sans-serif;'
        f'font-size:13px;color:#6c757d;'
        f'margin-bottom:12px;">'
        f'Salida #{ganador["salidas_actuales"]} '
        f'de {ganador["max_salidas"]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div style="background-color:#f1f3f5;'
        f'border-left:5px solid {ganador["color"]};'
        f'padding:14px 16px;border-radius:8px;'
        f'margin-bottom:14px;'
        f'font-family:Segoe UI,sans-serif;'
        f'font-size:15px;font-weight:600;'
        f'color:#212529;text-align:center;">'
        f'💡 "{st.session_state.pregunta_actual}"'
        f"</div>",
        unsafe_allow_html=True,
    )

    if st.button("🔄 Cambiar pregunta", use_container_width=True):

        otras = [
            p for p in ganador["preguntas"]
            if p != st.session_state.pregunta_actual
        ]

        st.session_state.pregunta_actual = (
            random.choice(otras)
            if otras
            else random.choice(ganador["preguntas"])
        )

        st.rerun()

    mins = st.session_state.tiempo_restante // 60
    segs = st.session_state.tiempo_restante % 60

    color_reloj = (
        "#dc3545"
        if st.session_state.tiempo_restante == 0
        else "#C44B56"
    )

    texto_reloj = (
        "¡TIEMPO!"
        if st.session_state.tiempo_restante == 0
        else f"{mins:02d}:{segs:02d}"
    )

    st.markdown(
        f'<div style="text-align:center;'
        f'font-family:Segoe UI,sans-serif;'
        f'font-size:36px;font-weight:800;'
        f'color:{color_reloj};background:#f8f9fa;'
        f'border-radius:10px;padding:10px;'
        f'margin:12px 0;">{texto_reloj}</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "▶ Iniciar",
            use_container_width=True,
            disabled=(st.session_state.tiempo_restante == 0),
        ):

            st.session_state.cronometro_activo = True
            st.rerun()

    with c2:

        if st.button(
            "⏸ Pausar",
            use_container_width=True,
            disabled=(st.session_state.tiempo_restante == 0),
        ):

            st.session_state.cronometro_activo = False
            st.rerun()

    if st.button(
        "⏹ Terminar",
        type="primary",
        use_container_width=True
    ):

        st.session_state.cronometro_activo = False
        st.session_state.sonar_campana = False

        transcurrido = (
            ganador["tiempo_inicial"]
            - st.session_state.tiempo_restante
        )

        m_t = transcurrido // 60
        s_t = transcurrido % 60

        duracion = f"{m_t:02d}:{s_t:02d}"

        st.session_state.historial.append(
            {
                "texto": (
                    f"{ganador['letra']} - {ganador['nombre']} "
                    f"(#{ganador['salidas_actuales']}) [{duracion}]"
                ),
                "color": ganador["color"],
            }
        )

        activas = [
            o for o in st.session_state.opciones
            if o["salidas_actuales"] < o["max_salidas"]
        ]

        if len(activas) == 0:

            st.session_state.estado_texto = (
                "¡Todas las categorías completaron sus 3 salidas!"
            )

        else:

            st.session_state.estado_texto = (
                f"Última: {ganador['nombre']} "
                f"(#{ganador['salidas_actuales']}/3) "
                f"| Activas: {len(activas)}"
            )

        st.session_state.mostrar_dialogo = False
        st.rerun()

    if (
        st.session_state.cronometro_activo
        and st.session_state.tiempo_restante > 0
    ):

        time.sleep(1)

        st.session_state.tiempo_restante -= 1

        if st.session_state.tiempo_restante == 0:

            st.session_state.cronometro_activo = False
            st.session_state.sonar_campana = True

        st.rerun()


# ==============================================================================
# 9. PESTAÑAS PRINCIPALES (RULETA Y NUBE DE IDEAS)
# ==============================================================================

tab_ruleta, tab_nube = st.tabs(
    ["🎯 Ruleta SCAMPER", "☁️ Nubecita de ideas"]
)


# ------------------------------------------------------------------------------
# PESTAÑA 1: RULETA
# ------------------------------------------------------------------------------

with tab_ruleta:

    col_izq, col_centro, col_der = st.columns(
        [1.25, 3.0, 1.35],
        gap="large"
    )

    with col_izq:

        dims_html = ""

        for dim in DIMENSIONES_SESION:

            dims_html += (
                f'<div class="item-dimension">'
                f'<div class="titulo-dimension">{dim["titulo"]}</div>'
                f'<div class="detalle-dimension">{dim["detalle"]}</div>'
                f"</div>"
            )

        st.markdown(
            f'<div class="panel-dimensiones">'
            f'<div class="titulo-historial">🧭 4 DIMENSIONES</div>'
            f"{dims_html}"
            f"</div>",
            unsafe_allow_html=True,
        )

    with col_centro:

        st.markdown(
            '<div class="titulo-scamper">SCAMPER</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="subtitulo-estado">'
            f'{st.session_state.estado_texto}</div>',
            unsafe_allow_html=True,
        )

        opciones_activas = [
            o for o in st.session_state.opciones
            if o["salidas_actuales"] < o["max_salidas"]
        ]

        placeholder_ruleta = st.empty()

        placeholder_ruleta.markdown(
            generar_svg_ruleta(
                opciones_activas,
                st.session_state.angulo_actual
            ),
            unsafe_allow_html=True,
        )

        st.markdown(
            generar_barra_vidas(st.session_state.opciones),
            unsafe_allow_html=True,
        )

        b1, b2 = st.columns(2, gap="medium")

        with b1:

            girar = st.button(
                "🎯 GIRAR RULETA",
                type="primary",
                use_container_width=True,
                disabled=(len(opciones_activas) == 0),
            )

        with b2:

            reiniciar = st.button(
                "🔄 Reiniciar",
                type="secondary",
                use_container_width=True,
            )

        if reiniciar:

            st.session_state.opciones = [
                {**item, "salidas_actuales": 0}
                for item in DATOS_SCAMPER
            ]

            st.session_state.historial = []
            st.session_state.angulo_actual = 0

            st.session_state.estado_texto = (
                "Opciones activas: 7 (máx. 3 salidas c/u)"
            )

            st.session_state.mostrar_dialogo = False
            st.session_state.cronometro_activo = False
            st.session_state.sonar_campana = False
            st.session_state.ganador_actual = None
            st.session_state.pregunta_actual = ""
            st.session_state.tiempo_restante = 90

            st.rerun()

        if girar and len(opciones_activas) > 0:

            indice_ganador = random.randrange(
                len(opciones_activas)
            )

            paso = 360.0 / len(opciones_activas)

            target_angle = (
                360.0
                - (indice_ganador * paso + paso / 2.0)
            ) % 360.0

            angulo_inicio = float(
                st.session_state.angulo_actual
            )

            recorrido = (
                target_angle - angulo_inicio
            ) % 360.0

            recorrido += 360.0 * random.randint(5, 7)

            pasos_animacion = 85

            for paso_animacion in range(pasos_animacion):

                progreso = (
                    paso_animacion + 1
                ) / pasos_animacion

                suavizado = 1 - (1 - progreso) ** 3

                angulo = (
                    angulo_inicio + recorrido * suavizado
                ) % 360.0

                st.session_state.angulo_actual = angulo

                placeholder_ruleta.markdown(
                    generar_svg_ruleta(
                        opciones_activas,
                        angulo
                    ),
                    unsafe_allow_html=True,
                )

                time.sleep(0.015)

            st.session_state.angulo_actual = target_angle

            ganador = opciones_activas[indice_ganador]

            ganador["salidas_actuales"] += 1

            st.session_state.ganador_actual = ganador

            st.session_state.pregunta_actual = random.choice(
                ganador["preguntas"]
            )

            st.session_state.tiempo_restante = (
                ganador["tiempo_inicial"]
            )

            st.session_state.cronometro_activo = False
            st.session_state.sonar_campana = False
            st.session_state.mostrar_dialogo = True

            activas_restantes = [
                o for o in st.session_state.opciones
                if o["salidas_actuales"] < o["max_salidas"]
            ]

            st.session_state.estado_texto = (
                f"Reto seleccionado: {ganador['nombre']} | "
                f"Salida #{ganador['salidas_actuales']} "
                f"de {ganador['max_salidas']} | "
                f"Activas: {len(activas_restantes)}"
            )

            st.rerun()

    with col_der:

        with st.container(border=True):

            st.markdown(
                '<div class="titulo-historial">'
                '📋 HISTORIAL DE SALIDAS</div>',
                unsafe_allow_html=True,
            )

            if st.session_state.historial:

                for item in reversed(
                    st.session_state.historial
                ):

                    texto_item = (
                        item["texto"]
                        if isinstance(item, dict)
                        else item
                    )

                    color_item = (
                        item["color"]
                        if isinstance(item, dict)
                        else "#C44B56"
                    )

                    st.markdown(
                        f'<div class="item-historial" '
                        f'style="border-left: 5px solid {color_item};">'
                        f"{texto_item}</div>",
                        unsafe_allow_html=True,
                    )

            else:

                st.caption(
                    "Aún no hay salidas registradas."
                )

        with st.container(border=True):

            st.markdown(
                '<div class="titulo-historial" '
                'style="margin-bottom:6px;">'
                '📱 CÓDIGO QR</div>',
                unsafe_allow_html=True,
            )

            st.image(
                crear_imagen_qr(
                    st.session_state.url_qr
                ),
                caption="Escanea para participar",
                use_container_width=True,
            )


# ------------------------------------------------------------------------------
# PESTAÑA 2: NUBECITA DE IDEAS (PROYECCIÓN EN SESIÓN)
# ------------------------------------------------------------------------------

with tab_nube:

    c_tit, c_btn = st.columns([4, 1])

    with c_tit:

        st.subheader(
            "☁️ Nubecita de ideas de la sesión"
        )

        st.caption(
            "Las ideas idénticas se agrupan automáticamente "
            "y crecen según cuántas veces se repiten."
        )

    with c_btn:

        if st.button(
            "🔄 Actualizar ideas",
            use_container_width=True
        ):

            st.session_state.refresco_nube += 1
            st.rerun()

    ideas_lista, error_lectura = leer_ideas_sheet(
        st.session_state.refresco_nube
    )

    if error_lectura:

        st.warning(error_lectura)

    elif not ideas_lista:

        st.info(
            "Aún no hay ideas registradas en la hoja 'Respuestas'."
        )

    else:

        burbujas = []

        for item in ideas_lista:

            tamano = min(
                28,
                15 + (item["cantidad"] - 1) * 3
            )

            borde = COLORES_LETRA.get(
                item["letra"],
                "#C44B56"
            )

            conteo = (
                f" <strong>(×{item['cantidad']})</strong>"
                if item["cantidad"] > 1
                else ""
            )

            etiqueta = (
                f"<span style='color:{borde}; font-weight:800;'>"
                f"[{item['letra']}]</span> "
                if item["letra"]
                else ""
            )

            burbujas.append(
                f'<div class="burbuja-nube" '
                f'style="font-size:{tamano}px; '
                f'border-color:{borde};">'
                f"{etiqueta}{item['idea']}{conteo}</div>"
            )

        st.markdown(
            f'<div class="nube-contenedor">'
            f'{"".join(burbujas)}</div>',
            unsafe_allow_html=True,
        )


# ==============================================================================
# 10. MOSTRAR VENTANA EMERGENTE
# ==============================================================================

if (
    st.session_state.mostrar_dialogo
    and st.session_state.ganador_actual
):

    dialogo_reto()
