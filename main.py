# -*- coding: utf-8 -*-
"""
Dashboard de Monitoreo Epidemiológico - Gusano Barrenador del Ganado
Sistema de visualización de datos para SENASICA
Estado de Yucatán, México
"""
import streamlit as st
from datetime import datetime

# Importar configuración
from src.config.settings import PAGE_CONFIG, TOTAL_MUNICIPIOS_YUCATAN
from src.config.styles import DASHBOARD_CSS

# Importar funciones de datos
from src.data.google_sheets import cargar_datos_desde_sheets, aplicar_filtros

# Importar utilidades
from src.utils.preparacion_datos import (
    agregar_coordenadas,
    preparar_datos_mapa,
    calcular_metricas_generales,
    obtener_top_municipios,
    preparar_datos_temporales,
    preparar_cronologia_primer_caso
)

# Importar componentes visuales
from src.components.graficas import (
    crear_mapa_casos,
    crear_grafica_barras_municipios,
    crear_grafica_casos_semanales,
    crear_cronologia_propagacion
)

# Importar análisis
from src.components.analisis import generar_recomendaciones

# Importar chatbot
from src.components.chatbot_ui import renderizar_chatbot_tab


# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================
st.set_page_config(**PAGE_CONFIG)

# Aplicar estilos CSS
st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)


# ============================================
# HEADER
# ============================================
st.markdown("""
<div class="gobierno-header">
    <h1>🇲🇽 Sistema de Monitoreo Epidemiológico - Gusano Barrenador del Ganado</h1>
    <h3>Estado de Yucatán | Servicio Nacional de Sanidad, Inocuidad y Calidad Agroalimentaria (SENASICA)<span class="badge-gobierno">2025</span></h3>
</div>
""", unsafe_allow_html=True)


# ============================================
# CARGAR DATOS
# ============================================
df = cargar_datos_desde_sheets()

if df.empty:
    st.error("❌ No se pudieron cargar los datos. Verifica la configuración de Google Sheets.")
    st.stop()


# ============================================
# SISTEMA DE NAVEGACIÓN
# ============================================
# Inicializar session state para la página activa
if 'pagina_activa' not in st.session_state:
    st.session_state.pagina_activa = "Dashboard"

# Selector de página en sidebar
with st.sidebar:
    st.markdown("### 📍 Navegación")
    pagina = st.radio(
        "Selecciona una página",
        ["📊 Dashboard Principal", "🤖 Asistente AI"],
        index=0 if st.session_state.pagina_activa == "Dashboard" else 1,
        label_visibility="collapsed"
    )

    # Actualizar estado
    if "Dashboard" in pagina:
        st.session_state.pagina_activa = "Dashboard"
    else:
        st.session_state.pagina_activa = "Asistente"

# ============================================
# FILTROS (aplicar a todas las páginas)
# ============================================
# Inicializar valores por defecto en session state
if 'municipio_seleccionado' not in st.session_state:
    st.session_state.municipio_seleccionado = ['Todos']
if 'fecha_inicio' not in st.session_state:
    st.session_state.fecha_inicio = df['Fecha_Reporte'].min().date()
if 'fecha_fin' not in st.session_state:
    st.session_state.fecha_fin = df['Fecha_Reporte'].max().date()

# Aplicar filtros usando valores de session state
df_filtrado = aplicar_filtros(
    df,
    st.session_state.municipio_seleccionado,
    st.session_state.fecha_inicio,
    st.session_state.fecha_fin
)

# Mostrar la página correspondiente
if st.session_state.pagina_activa == "Dashboard":
    # ============================================
    # CONTROLES DE FILTROS (solo en dashboard)
    # ============================================
    with st.expander("⚙️ OPCIONES DE FILTRADO Y ACTUALIZACIÓN", expanded=False):
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            municipios_disponibles = ['Todos'] + sorted(df['Municipio_Yucatan'].unique().tolist())
            municipio_sel = st.multiselect(
                "Filtrar por Municipio",
                municipios_disponibles,
                default=st.session_state.municipio_seleccionado
            )
            if municipio_sel != st.session_state.municipio_seleccionado:
                st.session_state.municipio_seleccionado = municipio_sel
                st.rerun()

        with col2:
            fecha_min = df['Fecha_Reporte'].min().date()
            fecha_max = df['Fecha_Reporte'].max().date()
            fechas = st.date_input(
                "Rango de Fechas",
                value=(st.session_state.fecha_inicio, st.session_state.fecha_fin),
                min_value=fecha_min,
                max_value=fecha_max
            )
            if len(fechas) == 2:
                if fechas[0] != st.session_state.fecha_inicio or fechas[1] != st.session_state.fecha_fin:
                    st.session_state.fecha_inicio, st.session_state.fecha_fin = fechas[0], fechas[1]
                    st.rerun()

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 ACTUALIZAR DATOS", width="stretch"):
                st.cache_data.clear()
                st.rerun()

    # ============================================
    # MÉTRICAS GENERALES
    # ============================================
    st.markdown('<p class="seccion-titulo">📊 Información General</p>', unsafe_allow_html=True)

    metricas = calcular_metricas_generales(df_filtrado)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="MUNICIPIOS AFECTADOS",
            value=f"{metricas['total_municipios']:,}"
        )

    with col2:
        st.metric(
            label="CASOS ACUMULADOS",
            value=f"{metricas['total_casos']:,}"
        )

    with col3:
        st.metric(
            label="CASOS ESTA SEMANA",
            value=f"{metricas['casos_semana']:,}"
        )

    with col4:
        st.metric(
            label="ÚLTIMA ACTUALIZACIÓN",
            value=metricas['ultima_fecha']
        )

    st.markdown("<br>", unsafe_allow_html=True)


    # ============================================
    # PREPARAR DATOS PARA VISUALIZACIONES
    # ============================================
    # Agregar coordenadas geográficas
    df_con_coords = agregar_coordenadas(df_filtrado)
    df_mapa = preparar_datos_mapa(df_con_coords)


    # ============================================
    # MAPA Y GRÁFICA DE BARRAS
    # ============================================
    col_izq, col_der = st.columns([1.8, 1.2], gap="large")

    with col_izq:
        st.markdown('<p class="seccion-titulo">🗺️ Mapa de Casos Confirmados</p>', unsafe_allow_html=True)
        st.markdown('<p style="color: #6c757d; font-size: 13px; margin-top: -10px;">(Seleccione una unidad o vista)</p>', unsafe_allow_html=True)

        fig_mapa = crear_mapa_casos(df_mapa)
        st.plotly_chart(fig_mapa, use_container_width=True, config={'displayModeBar': False})

    with col_der:
        st.markdown('<p class="seccion-titulo">📊 Municipios Más Afectados</p>', unsafe_allow_html=True)
        st.markdown('<p style="color: #6c757d; font-size: 13px; margin-top: -10px;">Top 10 de municipios con mayor número de casos</p>', unsafe_allow_html=True)

        top_municipios = obtener_top_municipios(df_filtrado, n=10)
        fig_barras = crear_grafica_barras_municipios(top_municipios)
        st.plotly_chart(fig_barras, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br><br>", unsafe_allow_html=True)


    # ============================================
    # ANÁLISIS TEMPORAL
    # ============================================
    st.markdown('<p class="seccion-titulo">📈 Análisis Temporal y de Propagación</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.5, 1], gap="large")

    with col1:
        st.markdown("**Evolución de Casos Semanales**")
        st.markdown('<p style="color: #6c757d; font-size: 12px; margin-top: -5px;">Casos reportados por semana con línea de tendencia</p>', unsafe_allow_html=True)

        df_tiempo = preparar_datos_temporales(df_filtrado)
        fig_linea = crear_grafica_casos_semanales(df_tiempo)
        st.plotly_chart(fig_linea, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown("**Datos Detallados por Municipio**")
        st.markdown('<p style="color: #6c757d; font-size: 12px; margin-top: -5px;">Municipios ordenados por casos totales</p>', unsafe_allow_html=True)

        df_tabla = df_filtrado[['Municipio_Yucatan', 'Casos_Acumulados']].groupby('Municipio_Yucatan').max().sort_values('Casos_Acumulados', ascending=False).reset_index()
        df_tabla.columns = ['Municipio', 'Casos Totales']

        st.dataframe(
            df_tabla.head(15),
            width="stretch",
            height=380,
            hide_index=True
        )

    st.markdown("<br>", unsafe_allow_html=True)


    # ============================================
    # CRONOLOGÍA DE PROPAGACIÓN
    # ============================================
    st.markdown("**Cronología de Propagación del Brote por Municipio**")
    st.markdown('<p style="color: #6c757d; font-size: 12px; margin-top: -5px;">Línea de tiempo mostrando cuándo se detectó el primer caso en cada municipio</p>', unsafe_allow_html=True)

    primer_caso_municipio = preparar_cronologia_primer_caso(df_filtrado)
    fig_cronologia = crear_cronologia_propagacion(primer_caso_municipio)
    st.plotly_chart(fig_cronologia, use_container_width=True, config={'displayModeBar': False})

    # Resumen de la cronología
    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)

    municipios_afectados = len(primer_caso_municipio)
    porcentaje_afectado = (municipios_afectados / TOTAL_MUNICIPIOS_YUCATAN) * 100
    primer_mun = primer_caso_municipio.iloc[0]['Municipio_Yucatan']
    primer_fecha = primer_caso_municipio.iloc[0]['Fecha_Reporte'].strftime('%d/%m/%Y')

    with col_a:
        st.metric("Total Municipios Afectados", f"{municipios_afectados}")
    with col_b:
        st.metric("% del Estado", f"{porcentaje_afectado:.1f}%")
    with col_c:
        st.metric("Primer Municipio", primer_mun)

    ultimo_mun = primer_caso_municipio.iloc[-1]['Municipio_Yucatan']
    ultima_fecha = primer_caso_municipio.iloc[-1]['Fecha_Reporte'].strftime('%d/%m/%Y')

    st.info(f"📍 **Brote iniciado:** {primer_mun} el {primer_fecha} | **Último municipio afectado:** {ultimo_mun} el {ultima_fecha}")


    # ============================================
    # CHATBOT DE ANÁLISIS
    # ============================================
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="seccion-titulo">🤖 Asistente de Análisis y Recomendaciones</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #6c757d; font-size: 13px; margin-top: -5px;">Análisis automatizado de datos y recomendaciones para la asignación de recursos</p>', unsafe_allow_html=True)

    col_opciones, col_resultado = st.columns([1, 2])

    with col_opciones:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <h4 style="color: #7D1F3A; margin-top: 0;">Selecciona un Análisis</h4>
        </div>
        """, unsafe_allow_html=True)

        tipo_analisis = st.radio(
            "Tipo de análisis",
            [
                "🎯 Municipios Prioritarios",
                "📈 Análisis de Tendencias",
                "💰 Apoyos Disponibles",
                "📦 Distribución de Recursos",
                "⚠️ Zonas de Alto Riesgo"
            ],
            key="tipo_analisis",
            label_visibility="collapsed"
        )

        generar_btn = st.button("🔍 GENERAR ANÁLISIS", width="stretch", type="primary")

        st.markdown("<br>", unsafe_allow_html=True)

        # Panel de información
        st.markdown(f"""
        <div style="background: #7D1F3A; color: white; padding: 20px; border-radius: 10px;">
            <h4 style="color: white; margin-top: 0; font-size: 16px;">📊 Resumen Actual</h4>
            <p style="font-size: 13px; margin: 8px 0;">
                <strong>Municipios afectados:</strong> {metricas['total_municipios']}<br>
                <strong>Casos totales:</strong> {metricas['total_casos']:,}<br>
                <strong>Casos esta semana:</strong> {metricas['casos_semana']:,}
            </p>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <h4 style="color: white; margin-top: 15px; font-size: 16px;">📞 Emergencias</h4>
            <p style="font-size: 12px; margin: 5px 0;">
                <strong>SENASICA:</strong><br>
                800-751-2100<br>
                WhatsApp: 55-3996-4462
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_resultado:
        if generar_btn:
            with st.spinner('Analizando datos...'):
                # Mapear el tipo de análisis
                tipo_map = {
                    "🎯 Municipios Prioritarios": "prioridad",
                    "📈 Análisis de Tendencias": "tendencia",
                    "💰 Apoyos Disponibles": "apoyos",
                    "📦 Distribución de Recursos": "distribucion",
                    "⚠️ Zonas de Alto Riesgo": "riesgo"
                }

                tipo_consulta = tipo_map[tipo_analisis]
                resultado = generar_recomendaciones(df_filtrado, tipo_consulta)

                st.markdown('<div style="background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid #7D1F3A; margin-top: 10px;">', unsafe_allow_html=True)
                st.markdown(resultado)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 40px; border-radius: 10px; text-align: center; border: 2px dashed #dee2e6;">
                <h3 style="color: #6c757d; font-size: 18px;">📊 Selecciona un tipo de análisis</h3>
                <p style="color: #999; font-size: 14px;">Elige una opción del menú izquierdo y haz clic en "Generar Análisis"</p>
            </div>
            """, unsafe_allow_html=True)


    # ============================================

else:  # Asistente AI
    # ============================================
    # ASISTENTE AI
    # ============================================
    renderizar_chatbot_tab(df_filtrado)


# FOOTER
# ============================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"""
<div class="footer-gobierno">
    <p><strong>📊 Fuente:</strong> SENASICA - Sistema Nacional de Vigilancia Epidemiológica | Gobierno de México</p>
    <p><strong>🕐 Actualizado:</strong> {datetime.now().strftime('%d de %B de %Y a las %H:%M hrs')}</p>
    <p><strong>📍 Ubicación:</strong> Estado de Yucatán, México | <strong>Total de Registros:</strong> {len(df_filtrado):,}</p>
    <p style="margin-top: 12px; font-size: 11px; color: #999;">Las vistas y series temporales consideran el lugar de residencia de los casos reportados</p>
</div>
""", unsafe_allow_html=True)
