# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 09:40:54 2026

@author: practicante-im
"""
import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import random
import time
import math

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS
# ==============================================================================
st.set_page_config(
    page_title="Ruleta SCAMPER - Comunicación de Equipo",
    page_icon="🎯",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f8f9fa;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
    max-width: 1380px;
}
.titulo-scamper {
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: #212529;
    letter-spacing: 3px;
    margin-bottom: 2px;
}
.subtitulo-estado {
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    font-size: 15px;
    font-weight: 500;
    color: #6c757d;
    margin-bottom: 8px;
}
.barra-vidas {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
    margin: 6px 0 16px 0;
}
.chip-vida {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 20px;
    padding: 4px 11px;
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
.panel-dimensiones {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 12px;
    padding: 16px 14px;
    min-height: 490px;
}
.item-dimension {
    background-color: #f8f9fa;
    border-left: 4px solid #C44B56;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 10px;
    font-family: 'Segoe UI', sans-serif;
}
.titulo-dimension {
    font-size: 13.5px;
    font-weight: 700;
    color: #212529;
    margin-bottom: 3px;
}
.detalle-dimension {
    font-size: 12px;
    color: #6c757d;
    line-height: 1.35;
}
.panel-historial {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 12px;
    padding: 15px 14px;
    height: 250px;
    overflow-y: auto;
    margin-bottom: 12px;
}
.panel-qr {
    background-color: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 12px;
    padding: 14px 14px;
    text-align: center;
}
.titulo-historial {
    text-align: center;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: #343a40;
    margin-bottom: 12px;
    letter-spacing: 0.5px;
}
.item-historial {
    background-color: #f1f3f5;
    color: #212529;
    padding: 8px 10px;
    margin-bottom: 7px;
    border-radius: 8px;
    border-left: 5px solid #C44B56;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
    font-weight: 700;
}
div.stButton > button {
    border-radius: 10px;
    font-family: 'Segoe UI', sans-serif;
    font-weight: 700;
    font-size: 15px;
    padding: 12px 18px;
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
""", unsafe_allow_html=True)

# ==============================================================================
# 2. 4 DIMENSIONES DE REFERENCIA (COLUMNA IZQUIERDA)
# ==============================================================================
DIMENSIONES_SESION = [
    {
        "icono": "💬",
        "titulo": "Comunicación",
        "detalle": "Escucharnos, conversar y compartir nuestras ideas.",
        "color": "#C44B56"
    },
    {
        "icono": "🤝",
        "titulo": "Compañerismo",
        "detalle": "Conocernos, apoyarnos y generar cercanía.",
        "color": "#F2897B"
    },
    {
        "icono": "🧩",
        "titulo": "Colaboración",
        "detalle": "Integrar las tres áreas y compartir conocimientos.",
        "color": "#F3A155"
    },
    {
        "icono": "🎯",
        "titulo": "Trabajo en equipo",
        "detalle": "Coordinar esfuerzos y alcanzar objetivos comunes.",
        "color": "#A392AF"
    },
]

# ==============================================================================
# 3. DATOS SCAMPER: PALETA SIN OLIVE GREEN + PREGUNTAS DE COMUNICACIÓN
# ==============================================================================
DATOS_SCAMPER = [
    {
        "letra": "S", "nombre": "SUSTITUIR", "color": "#C44B56", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "¿Qué podríamos cambiar en nuestra forma de comunicarnos para generar conversaciones más abiertas y cercanas entre compañeros?",
            "¿Qué hábitos de comunicación deberíamos sustituir para evitar malentendidos entre las tres áreas?"
        ]
    },
    {
        "letra": "C", "nombre": "COMBINAR", "color": "#F2897B", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "¿Qué espacios podríamos crear o combinar para compartir no solamente temas de trabajo, sino también experiencias e intereses como compañeros?",
            "¿Cómo podríamos integrar mejor los conocimientos y perspectivas de Innovación, Investigación y Voz del Cliente mediante una comunicación más fluida?"
        ]
    },
    {
        "letra": "A", "nombre": "ADAPTAR", "color": "#F3A155", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "¿Qué buenas prácticas de comunicación podríamos adoptar para escucharnos y comprendernos mejor como equipo?",
            "¿Cómo podríamos adaptar nuestra forma de compartir información para que las otras áreas comprendan mejor nuestro trabajo?"
        ]
    },
    {
        "letra": "M", "nombre": "MODIFICAR", "color": "#F5D687", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "¿Qué podríamos cambiar en nuestras conversaciones y reuniones para que todos tengamos más oportunidades de participar y expresar nuestras ideas?",
            "¿Cómo podríamos mejorar la manera en que nos comunicamos cuando necesitamos apoyo o colaboración de otros compañeros?"
        ]
    },
    {
        "letra": "P", "nombre": "PONER EN OTROS USOS", "color": "#6C7F54", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "¿Cómo podríamos aprovechar los espacios que ya compartimos para conocernos mejor y fortalecer nuestra comunicación como compañeros?",
            "¿Cómo podríamos aprovechar las fortalezas y conocimientos de cada compañero para apoyarnos mutuamente?"
        ]
    },
    {
        "letra": "E", "nombre": "ELIMINAR", "color": "#B3CFC3", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "¿Qué barreras o hábitos de comunicación deberíamos dejar atrás para relacionarnos mejor como compañeros y sentirnos más conectados como equipo?",
            "¿Qué situaciones hacen que a veces no compartamos nuestras ideas, inquietudes o necesidades con los demás?"
        ]
    },
    {
        "letra": "R", "nombre": "REORDENAR", "color": "#A392AF", "tiempo_inicial": 90, "max_salidas": 3,
        "preguntas": [
            "¿Cómo podríamos reorganizar nuestras dinámicas de comunicación y trabajo para estar más conectados como equipo e involucrar a las tres áreas desde el inicio de los proyectos?",
            "¿Cómo podríamos generar más oportunidades para conversar, compartir y colaborar entre compañeros, incluso cuando no estamos trabajando en un mismo proyecto?"
        ]
    }
]

URL_APP_DESTINO_DEFAULT = ""

def inicializar_estado():
    if "opciones" not in st.session_state:
        st.session_state.opciones = [{**item, "salidas_actuales": 0} for item in DATOS_SCAMPER]
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
        st.session_state.url_qr = URL_APP_DESTINO_DEFAULT

inicializar_estado()

# ==============================================================================
# 4. SONIDO DE CAMPANA
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
                    gain.gain.exponentialRampToValueAtTime(0.001, inicio + duracion);
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
        width=0
    )

# ==============================================================================
# 5. DIBUJO DE LA RULETA CIRCULAR E INDICADOR DE VIDAS
# ==============================================================================
def generar_svg_ruleta(opciones, angulo_actual):
    size = 420
    cx = size / 2
    cy = size / 2
    r = 180
    num = len(opciones)

    if num == 0:
        return (
            f'<div style="display:flex;justify-content:center;align-items:center;margin:6px 0;">'
            f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f8f9fa" stroke="#dee2e6" stroke-width="3"/>'
            f'<text x="{cx}" y="{cy}" fill="#495057" font-family="Segoe UI, sans-serif" '
            f'font-size="22" font-weight="bold" text-anchor="middle" dominant-baseline="middle">'
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
            partes.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{opt["color"]}" stroke="white" stroke-width="3"/>')
        else:
            d = f"M {cx},{cy} L {x1:.2f},{y1:.2f} A {r},{r} 0 {large_arc},1 {x2:.2f},{y2:.2f} Z"
            partes.append(f'<path d="{d}" fill="{opt["color"]}" stroke="white" stroke-width="3"/>')

        mid_deg = start_deg + (paso / 2.0)
        rot_texto = mid_deg - 90
        mid_rad = math.radians(rot_texto)
        tx = cx + (r * 0.56) * math.cos(mid_rad)
        ty = cy + (r * 0.56) * math.sin(mid_rad)

        font_size = 10 if len(opt["nombre"]) > 14 else 11.5
        color_texto = "#212529" if opt["color"] in ["#F5D687", "#B3CFC3"] else "#ffffff"
        partes.append(
            f'<text x="{tx:.2f}" y="{ty:.2f}" fill="{color_texto}" font-family="Segoe UI, sans-serif" '
            f'font-size="{font_size}" font-weight="bold" text-anchor="middle" dominant-baseline="middle" '
            f'transform="rotate({rot_texto:.2f}, {tx:.2f}, {ty:.2f})">{opt["nombre"]}</text>'
        )

    centro_y_flecha = (
        f'<circle cx="{cx}" cy="{cy}" r="{r * 0.16:.1f}" fill="#ffffff" stroke="#c8c8c8" stroke-width="3"/>'
        f'<polygon points="{cx},{cy - r - 15} {cx - 13},{cy - r + 4} {cx + 13},{cy - r + 4}" fill="#212529"/>'
    )

    return (
        f'<div style="display:flex;justify-content:center;align-items:center;margin:2px 0 6px 0;">'
        f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">'
        f'{"".join(partes)}{centro_y_flecha}'
        f'</svg></div>'
    )

def generar_barra_vidas(todas_opciones):
    chips = []
    for opt in todas_opciones:
        restantes = opt["max_salidas"] - opt["salidas_actuales"]
        puntos = ("● " * restantes + "○ " * opt["salidas_actuales"]).strip()
        opacidad = "1" if restantes > 0 else "0.45"
        color_letra = opt["color"] if restantes > 0 else "#6c757d"
        chips.append(
            f'<div class="chip-vida" style="opacity:{opacidad};">'
            f'<span style="color:{color_letra};font-size:15px;font-weight:900;">{opt["letra"]}</span>'
            f'<span style="color:{color_letra};letter-spacing:1px;">{puntos}</span>'
            f'</div>'
        )
    return f'<div class="barra-vidas">{"".join(chips)}</div>'

# ==============================================================================
# 6. VENTANA EMERGENTE DEL RETO
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
        f'<div style="text-align:center;font-family:Segoe UI,sans-serif;font-size:46px;'
        f'font-weight:800;color:{ganador["color"]};line-height:1.1;text-shadow: 1px 1px 2px rgba(0,0,0,0.08);">{ganador["letra"]} - {ganador["nombre"]}</div>'
        f'<div style="text-align:center;font-family:Segoe UI,sans-serif;font-size:13px;'
        f'color:#6c757d;margin-bottom:12px;">Salida #{ganador["salidas_actuales"]} de {ganador["max_salidas"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div style="background-color:#f1f3f5;border-left:5px solid {ganador["color"]};'
        f'padding:14px 16px;border-radius:8px;margin-bottom:14px;font-family:Segoe UI,sans-serif;'
        f'font-size:15px;font-weight:600;color:#212529;text-align:center;">'
        f'💡 "{st.session_state.pregunta_actual}"'
        f'</div>',
        unsafe_allow_html=True
    )

    if st.button("🔄 Cambiar pregunta", use_container_width=True):
        otras = [p for p in ganador["preguntas"] if p != st.session_state.pregunta_actual]
        st.session_state.pregunta_actual = random.choice(otras) if otras else random.choice(ganador["preguntas"])
        st.rerun()

    mins = st.session_state.tiempo_restante // 60
    segs = st.session_state.tiempo_restante % 60
    color_reloj = "#dc3545" if st.session_state.tiempo_restante == 0 else "#C44B56"
    texto_reloj = "¡TIEMPO!" if st.session_state.tiempo_restante == 0 else f"{mins:02d}:{segs:02d}"

    st.markdown(
        f'<div style="text-align:center;font-family:Segoe UI,sans-serif;font-size:38px;'
        f'font-weight:800;color:{color_reloj};background:#f8f9fa;border-radius:10px;padding:10px;'
        f'margin:12px 0;">{texto_reloj}</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("▶ Iniciar", use_container_width=True, disabled=(st.session_state.tiempo_restante == 0)):
            st.session_state.cronometro_activo = True
            st.rerun()
    with c2:
        if st.button("⏸ Pausar", use_container_width=True, disabled=(st.session_state.tiempo_restante == 0)):
            st.session_state.cronometro_activo = False
            st.rerun()

    if st.button("⏹ Terminar", type="primary", use_container_width=True):
        st.session_state.cronometro_activo = False
        st.session_state.sonar_campana = False
        transcurrido = ganador["tiempo_inicial"] - st.session_state.tiempo_restante
        m_t = transcurrido // 60
        s_t = transcurrido % 60
        duracion = f"{m_t:02d}:{s_t:02d}"

        st.session_state.historial.append(
            f"{ganador['letra']} - {ganador['nombre']} (#{ganador['salidas_actuales']}) [{duracion}]"
        )
        activas = [o for o in st.session_state.opciones if o["salidas_actuales"] < o["max_salidas"]]
        if len(activas) == 0:
            st.session_state.estado_texto = "¡Todas las categorías completaron sus 3 salidas!"
        else:
            st.session_state.estado_texto = f"Última: {ganador['nombre']} (#{ganador['salidas_actuales']}/3) | Activas: {len(activas)}"

        st.session_state.mostrar_dialogo = False
        st.rerun()

    if st.session_state.cronometro_activo and st.session_state.tiempo_restante > 0:
        time.sleep(1)
        st.session_state.tiempo_restante -= 1
        if st.session_state.tiempo_restante == 0:
            st.session_state.cronometro_activo = False
            st.session_state.sonar_campana = True
        st.rerun()

# ==============================================================================
# 7. INTERFAZ PRINCIPAL (3 COLUMNAS: DIMENSIONES | RULETA | HISTORIAL + QR)
# ==============================================================================
col_izq, col_centro, col_der = st.columns([1.25, 3.0, 1.25], gap="large")

with col_izq:
    dims_html = ""
    for dim in DIMENSIONES_SESION:
        dims_html += (
            f'<div class="item-dimension" style="border-left-color:{dim["color"]};">'
            f'<div style="font-size:15px;line-height:1;margin-bottom:4px;">{dim["icono"]}</div>'
            f'<div class="titulo-dimension">{dim["titulo"]}</div>'
            f'<div class="detalle-dimension">{dim["detalle"]}</div>'
            f'</div>'
        )

    html_dimensiones = (
        '<div class="panel-dimensiones">'
        '<div class="titulo-historial">4 DIMENSIONES</div>'
        f'{dims_html}'
        '</div>'
    )
    st.markdown(html_dimensiones, unsafe_allow_html=True)

with col_centro:
    st.markdown('<div class="titulo-scamper">SCAMPER</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitulo-estado">{st.session_state.estado_texto}</div>', unsafe_allow_html=True)

    opciones_activas = [o for o in st.session_state.opciones if o["salidas_actuales"] < o["max_salidas"]]
    placeholder_ruleta = st.empty()
    placeholder_ruleta.markdown(generar_svg_ruleta(opciones_activas, st.session_state.angulo_actual), unsafe_allow_html=True)

    st.markdown(generar_barra_vidas(st.session_state.opciones), unsafe_allow_html=True)

    b1, b2 = st.columns(2, gap="medium")
    with b1:
        girar = st.button("🎯 GIRAR RULETA", type="primary", use_container_width=True, disabled=(len(opciones_activas) == 0))
    with b2:
        reiniciar = st.button("🔄 Reiniciar", type="secondary", use_container_width=True)

    if reiniciar:
        st.session_state.opciones = [{**item, "salidas_actuales": 0} for item in DATOS_SCAMPER]
        st.session_state.historial = []
        st.session_state.angulo_actual = 0
        st.session_state.estado_texto = "Opciones activas: 7 (máx. 3 salidas c/u)"
        st.session_state.mostrar_dialogo = False
        st.session_state.cronometro_activo = False
        st.session_state.sonar_campana = False
        st.rerun()

    if girar and len(opciones_activas) > 0:
        velocidad = random.uniform(38, 52)
        while velocidad > 1.2:
            st.session_state.angulo_actual = (st.session_state.angulo_actual + velocidad) % 360
            placeholder_ruleta.markdown(
                generar_svg_ruleta(opciones_activas, st.session_state.angulo_actual),
                unsafe_allow_html=True
            )
            velocidad *= 0.88
            time.sleep(0.04)

        paso = 360.0 / len(opciones_activas)
        angulo_flecha = (360.0 - st.session_state.angulo_actual) % 360.0
        indice_ganador = int(angulo_flecha / paso) % len(opciones_activas)
        ganador = opciones_activas[indice_ganador]

        ganador["salidas_actuales"] += 1
        st.session_state.ganador_actual = ganador
        st.session_state.pregunta_actual = random.choice(ganador["preguntas"])
        st.session_state.tiempo_restante = ganador["tiempo_inicial"]
        st.session_state.cronometro_activo = False
        st.session_state.sonar_campana = False
        st.session_state.mostrar_dialogo = True
        st.rerun()

with col_der:
    items_html = ""
    for entry in st.session_state.historial:
        items_html += f'<div class="item-historial">{entry}</div>'

    html_panel = (
        '<div class="panel-historial">'
        '<div class="titulo-historial">HISTORIAL DE SALIDAS</div>'
        f'{items_html}'
        '</div>'
    )
    st.markdown(html_panel, unsafe_allow_html=True)

    if st.session_state.url_qr.strip():
        url_codificada = urllib.parse.quote(st.session_state.url_qr.strip(), safe="")
        qr_contenido = f'<img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={url_codificada}" width="135" height="135" style="border-radius:8px;margin:2px 0 6px 0;" />'
    else:
        qr_contenido = (
            '<div style="width:135px;height:135px;margin:2px auto 6px auto;border:2px dashed #ced4da;'
            'border-radius:8px;display:flex;align-items:center;justify-content:center;color:#adb5bd;'
            'font-family:Segoe UI,sans-serif;font-size:12px;padding:8px;">Espacio reservado para tu QR</div>'
        )

    html_qr = (
        '<div class="panel-qr">'
        '<div class="titulo-historial" style="margin-bottom:6px;">📱 SIGUIENTE PASO</div>'
        f'{qr_contenido}'
        '<div style="font-family:Segoe UI,sans-serif;font-size:12px;color:#6c757d;">'
        'Escanea para ingresar tu idea'
        '</div>'
        '</div>'
    )
    st.markdown(html_qr, unsafe_allow_html=True)

    with st.expander("🔗 Configurar enlace del QR", expanded=False):
        nueva_url = st.text_input("Pega aquí el link de tu app:", value=st.session_state.url_qr, label_visibility="collapsed", placeholder="https://...")
        if nueva_url != st.session_state.url_qr:
            st.session_state.url_qr = nueva_url
            st.rerun()

if st.session_state.mostrar_dialogo:
    dialogo_reto()