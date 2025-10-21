# -*- coding: utf-8 -*-
"""
Componentes de interfaz para el asistente AI del dashboard
Incluye el drawer (panel lateral) y la página completa de análisis
"""
import streamlit as st
from datetime import datetime
from typing import Optional
import uuid
import pandas as pd

from src.agents.consejo_rapido_agent import ConsejoRapidoAgent
from src.agents.analisis_completo_agent import AnalisisCompletoAgent


def inicializar_session_state():
    """Inicializa las variables de sesión necesarias para el chatbot"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if 'chat_history_full' not in st.session_state:
        st.session_state.chat_history_full = []


def preparar_contexto_datos(df):
    """Prepara un resumen de los datos actuales para el contexto del agente"""
    total_municipios = df['Municipio_Yucatan'].nunique()
    total_casos = df['Casos_Acumulados'].max()

    # Obtener top 5 municipios
    top_municipios = df.groupby('Municipio_Yucatan')['Casos_Acumulados'].max().sort_values(ascending=False).head(5)
    top_list = "\n".join([f"- {mun}: {casos} casos" for mun, casos in top_municipios.items()])

    # Casos recientes
    fecha_max = df['Fecha_Reporte'].max()
    semana_actual = df[df['Fecha_Reporte'] >= (fecha_max - pd.Timedelta(days=7))]
    casos_semana = len(semana_actual)

    contexto = f"""
DATOS ACTUALES DE YUCATÁN (actualizado: {fecha_max.strftime('%d/%m/%Y')}):
- Total de municipios afectados: {total_municipios}
- Total de casos acumulados: {total_casos}
- Casos en la última semana: {casos_semana}

Top 5 municipios más afectados:
{top_list}

Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}
"""
    return contexto


def renderizar_drawer(df):
    """
    Renderiza el drawer (panel lateral pequeño) con consejos rápidos
    ELIMINADO - Ya no se usa, quedó muy complicado
    """
    pass


def renderizar_pagina_completa(df):
    """
    Renderiza la página completa del asistente AI con análisis profundo

    Args:
        df: DataFrame con los datos actuales del dashboard
    """
    inicializar_session_state()

    st.markdown('<div class="seccion-titulo">🤖 VetAI - Asistente Epidemiológico</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6c757d; font-size: 13px; margin-top: -5px;">Análisis profundo con búsqueda web y contexto global del gusano barrenador</p>', unsafe_allow_html=True)

    # Inicializar agente
    api_key = st.secrets["anthropic"]["api_key"]
    contexto = preparar_contexto_datos(df)

    if 'agente_completo' not in st.session_state:
        st.session_state.agente_completo = AnalisisCompletoAgent(
            api_key=api_key,
            datos_contexto=contexto
        )

    # Barra superior con controles
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        usar_web = st.checkbox(
            "🌐 Incluir búsqueda web",
            value=True,
            help="Buscar información adicional en internet"
        )

    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 8px; background: #7D1F3A; color: white; border-radius: 5px; font-size: 12px;">
            📊 {df['Municipio_Yucatan'].nunique()} municipios | {df['Casos_Acumulados'].max():,} casos
        </div>
        """, unsafe_allow_html=True)

    with col3:
        if st.button("🗑️ Limpiar historial", use_container_width=True):
            st.session_state.chat_history_full = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()

    with col4:
        if st.session_state.chat_history_full:
            export_text = f"# Conversación del Asistente AI\n# Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
            for chat in st.session_state.chat_history_full:
                export_text += f"## Pregunta ({chat['timestamp'].strftime('%H:%M')})\n{chat['pregunta']}\n\n"
                export_text += f"## Respuesta\n{chat['respuesta']}\n\n"
                if chat.get('fuentes'):
                    export_text += f"**Fuentes:** {', '.join(chat['fuentes'])}\n\n"
                export_text += "---\n\n"

            st.download_button(
                label="💾 Exportar",
                data=export_text,
                file_name=f"analisis_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Preguntas sugeridas en línea horizontal
    st.markdown("**📝 Análisis Sugeridos:**")

    preguntas_complejas = [
        "Compara con brotes históricos",
        "Mejores prácticas internacionales",
        "Patrón de propagación y predicción",
        "Medidas de otros países",
        "Impacto económico",
        "Recursos internacionales"
    ]

    cols = st.columns(3)
    pregunta_del_boton = None

    for i, pregunta in enumerate(preguntas_complejas):
        with cols[i % 3]:
            if st.button(pregunta, key=f"sug_{i}", use_container_width=True):
                # Expandir la pregunta a su versión completa
                preguntas_completas = [
                    "Compara la situación de Yucatán con otros brotes históricos de gusano barrenador",
                    "¿Cuáles son las mejores prácticas internacionales para contener este brote?",
                    "Analiza el patrón de propagación y predice posibles municipios en riesgo",
                    "¿Qué medidas han tomado otros países en situaciones similares?",
                    "Evalúa el impacto económico del brote en la ganadería local",
                    "¿Qué recursos de organismos internacionales (FAO, OIE) están disponibles?"
                ]
                pregunta_del_boton = preguntas_completas[i]

    st.markdown("<br>", unsafe_allow_html=True)

    # Área de chat
    if st.session_state.chat_history_full:
        for chat in st.session_state.chat_history_full:
            # Mensaje del usuario
            with st.container():
                st.markdown(f"""
                <div style="background: #f0f0f0; padding: 15px 20px; border-radius: 10px;
                            margin-bottom: 15px; max-width: 85%; margin-left: auto;">
                    <div style="font-size: 11px; color: #999; margin-bottom: 5px;">
                        🙋 Tú • {chat['timestamp'].strftime('%d/%m/%Y %H:%M')}
                    </div>
                    <div style="color: #333;">
                        {chat['pregunta']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Respuesta del asistente
            with st.container():
                st.markdown(f"""
                <div style="background: #e8f4f8; padding: 20px 20px 10px 20px; border-radius: 10px;
                            margin-bottom: 25px; max-width: 85%; border-left: 4px solid #7D1F3A;">
                    <div style="font-size: 11px; color: #666; margin-bottom: 10px;">
                        🤖 VetAI
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Renderizar el markdown de la respuesta usando st.markdown nativo
                st.markdown(chat['respuesta'])

                # Fuentes si hay
                if chat.get('fuentes'):
                    st.markdown(f"**🔍 Fuentes:** {', '.join(chat['fuentes'])}")

                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 80px 40px; color: #999;">
            <h2 style="color: #7D1F3A; margin-bottom: 15px;">👋 ¡Hola! Soy VetAI</h2>
            <p style="font-size: 16px; color: #666; max-width: 600px; margin: 0 auto;">
                Tu asistente especializado en análisis epidemiológico del gusano barrenador.<br>
                Puedo analizar los datos de Yucatán y buscar información global sobre
                mejores prácticas y estrategias de contención.
            </p>
            <p style="margin-top: 20px; color: #7D1F3A; font-weight: 500;">
                Selecciona un análisis sugerido o escribe tu pregunta abajo
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Input de pregunta
    pregunta = st.text_area(
        "Escribe tu pregunta o solicitud de análisis:",
        value=pregunta_del_boton if pregunta_del_boton else "",
        height=120,
        key=f"full_input_{st.session_state.session_id}",
        placeholder="Ejemplo: Analiza el patrón de propagación del brote y compáralo con otros casos documentados en América Latina..."
    )

    col_btn1, col_btn2, col_btn3 = st.columns([1, 5, 1])

    with col_btn1:
        enviar = st.button("📤 Analizar", type="primary", use_container_width=True)

    # Procesar pregunta
    if (enviar and pregunta) or pregunta_del_boton:
        pregunta_a_enviar = pregunta if pregunta else pregunta_del_boton

        if pregunta_a_enviar:
            # Mostrar status mientras procesa
            with st.status("🤖 VetAI está analizando...", expanded=True) as status:
                if usar_web:
                    st.write("🌐 Buscando información en internet...")
                st.write("📊 Analizando datos de Yucatán...")
                st.write("💡 Generando recomendaciones...")

                resultado = st.session_state.agente_completo.analizar(
                    pregunta_a_enviar,
                    session_id=st.session_state.session_id,
                    usar_busqueda_web=usar_web
                )

                status.update(label="✅ VetAI completó el análisis!", state="complete", expanded=False)

            st.session_state.chat_history_full.append({
                "pregunta": pregunta_a_enviar,
                "respuesta": resultado['respuesta'],
                "fuentes": resultado.get('fuentes', []),
                "timestamp": datetime.now()
            })

            st.rerun()


def renderizar_chatbot_tab(df):
    """
    Renderiza la pestaña completa del chatbot
    (wrapper para integración con main.py)

    Args:
        df: DataFrame con los datos actuales del dashboard
    """
    renderizar_pagina_completa(df)
