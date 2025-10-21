"""
CSS Modular con selectores específicos para cada elemento
Cada texto tiene su propio color asignado sin afectar otros elementos
"""

DASHBOARD_CSS = """
<style>
    /* ==================== FUENTE BASE ==================== */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');

    /* Aplicar fuente solo a elementos específicos de Streamlit, NO usar selector universal */
    .stApp,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    .stApp p, .stApp span, .stApp div,
    .stButton button,
    [data-testid="stSidebar"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        font-family: 'Montserrat', sans-serif;
    }

    /* ==================== CONFIGURACIÓN GENERAL ==================== */
    .stApp {
        background-color: #f5f5f5;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Ocultar badges y elementos de Streamlit que no queremos */
    [data-testid="stStatusWidget"] div[data-testid="stMarkdownContainer"] {
        display: none !important;
    }

    /* Ocultar el texto "streamlitApp" que aparece arriba */
    iframe[title="streamlitApp"] {
        display: none !important;
    }

    /* ==================== HEADER GUBERNAMENTAL ==================== */
    /* Solo afecta al div con clase gobierno-header */
    .gobierno-header {
        background: linear-gradient(135deg, #7D1F3A 0%, #5D1729 100%);
        padding: 28px 40px;
        border-radius: 0;
        margin: -60px -60px 30px -60px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* Título principal del header - BLANCO */
    .gobierno-header h1 {
        color: #FFFFFF !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        padding: 0 !important;
        letter-spacing: -0.5px !important;
    }

    /* Subtítulo del header - DORADO */
    .gobierno-header h3 {
        color: #C4A772 !important;
        font-size: 15px !important;
        font-weight: 400 !important;
        margin: 8px 0 0 0 !important;
        padding: 0 !important;
    }

    /* Badge del año - GUINDA sobre DORADO */
    .badge-gobierno {
        display: inline-block;
        background: #C4A772;
        color: #7D1F3A;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 15px;
    }

    /* ==================== SIDEBAR ==================== */
    /* Fondo del sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    /* Títulos del sidebar - NEGRO */
    [data-testid="stSidebar"] h3 {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* Labels del sidebar - NEGRO */
    [data-testid="stSidebar"] label {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* Párrafos del sidebar - NEGRO */
    [data-testid="stSidebar"] p {
        color: #000000 !important;
    }

    /* ==================== MÉTRICAS ==================== */
    /* Contenedor de métricas */
    div[data-testid="metric-container"] {
        background: white;
        padding: 30px 24px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 4px solid #7D1F3A;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(125, 31, 58, 0.15);
    }

    /* Label de métrica - GRIS */
    [data-testid="stMetricLabel"] {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #6c757d !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        margin-bottom: 8px !important;
    }

    /* Valor de métrica - GUINDA */
    [data-testid="stMetricValue"] {
        font-size: 42px !important;
        font-weight: 800 !important;
        color: #7D1F3A !important;
        line-height: 1 !important;
    }

    /* ==================== TÍTULOS DE SECCIÓN ==================== */
    /* Solo afecta a elementos con clase seccion-titulo */
    .seccion-titulo {
        color: #2c3e50 !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        margin: 30px 0 16px 0 !important;
        padding-left: 12px !important;
        border-left: 4px solid #7D1F3A !important;
    }

    /* ==================== BOTONES ==================== */
    /* Solo afecta a botones de Streamlit */
    .stButton button {
        background: linear-gradient(135deg, #7D1F3A 0%, #5D1729 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s;
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #5D1729 0%, #4D1220 100%);
        box-shadow: 0 6px 12px rgba(125, 31, 58, 0.3);
        transform: translateY(-1px);
    }

    /* ==================== EXPANDERS ==================== */
    /* Header del expander - NEGRO */
    .streamlit-expanderHeader {
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        color: #000000 !important;
    }

    /* ==================== INPUTS Y LABELS ==================== */
    /* Labels de inputs - NEGRO */
    .stTextInput label,
    .stSelectbox label,
    .stMultiSelect label,
    .stTextArea label,
    .stCheckbox label {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* Radio buttons - NEGRO */
    [data-testid="stRadio"] label {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* ==================== TABLAS ==================== */
    /* Tabla de Streamlit */
    .dataframe {
        font-size: 13px !important;
    }

    /* Header de tabla - BLANCO sobre GUINDA */
    .dataframe thead tr th {
        background-color: #7D1F3A !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        padding: 12px 8px !important;
    }

    /* Celdas de tabla - NEGRO sobre BLANCO */
    .dataframe tbody tr td {
        color: #000000 !important;
        background-color: white !important;
    }

    /* ==================== GRÁFICAS PLOTLY ==================== */
    /* NO tocar las gráficas - Plotly maneja sus propios estilos */
    /* Dejar que los textos de Plotly se rendericen con sus colores por defecto */

    /* ==================== CHATBOT ==================== */
    /* Mensaje del usuario - GRIS sobre FONDO CLARO */
    .mensaje-usuario {
        background: #f0f0f0;
        padding: 15px 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        max-width: 85%;
        margin-left: auto;
    }

    .mensaje-usuario-timestamp {
        font-size: 11px;
        color: #999999;
        margin-bottom: 5px;
    }

    .mensaje-usuario-texto {
        color: #333333;
    }

    /* Respuesta del asistente - BLANCO sobre GUINDA */
    .respuesta-asistente {
        background: #7D1F3A;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        max-width: 85%;
    }

    .respuesta-asistente-header {
        font-size: 11px;
        color: #FFFFFF;
        margin-bottom: 10px;
    }

    /* TODO el texto dentro de respuesta-asistente debe ser BLANCO */
    .respuesta-asistente p,
    .respuesta-asistente h1,
    .respuesta-asistente h2,
    .respuesta-asistente h3,
    .respuesta-asistente h4,
    .respuesta-asistente li,
    .respuesta-asistente ul,
    .respuesta-asistente ol,
    .respuesta-asistente span,
    .respuesta-asistente strong,
    .respuesta-asistente em,
    .respuesta-asistente code,
    .respuesta-asistente a {
        color: #FFFFFF !important;
    }

    /* ==================== PANEL DE RESUMEN (GUINDA) ==================== */
    .panel-guinda {
        background: #7D1F3A;
        padding: 20px;
        border-radius: 10px;
    }

    /* Todo el texto del panel guinda debe ser BLANCO */
    .panel-guinda h4,
    .panel-guinda p,
    .panel-guinda span,
    .panel-guinda strong {
        color: #FFFFFF !important;
    }

    /* ==================== FOOTER ==================== */
    .footer-gobierno {
        background: white;
        padding: 20px;
        border-radius: 8px;
        margin-top: 40px;
        border-top: 3px solid #7D1F3A;
    }

    /* Texto del footer - GRIS */
    .footer-gobierno p {
        color: #6c757d !important;
        font-size: 13px;
        margin: 5px 0;
    }

    /* ==================== TEXTOS DESCRIPTIVOS ==================== */
    /* Subtítulos de gráficas - GRIS */
    .texto-subtitulo-grafica {
        color: #6c757d;
        font-size: 13px;
        margin-top: -10px;
    }

    /* ==================== STATUS Y SPINNERS ==================== */
    /* Textos dentro de status/spinner - NEGRO */
    [data-testid="stStatusWidget"] p {
        color: #000000 !important;
    }

    /* ==================== CONTENIDO DE ANÁLISIS Y MARKDOWN ==================== */
    /* Asegurar que todo el markdown tenga colores correctos */

    /* Markdown en main area - NEGRO por defecto */
    .main div[data-testid="stMarkdownContainer"] p,
    .main div[data-testid="stMarkdownContainer"] li,
    .main div[data-testid="stMarkdownContainer"] span {
        color: #000000 !important;
    }

    /* Títulos en markdown - GUINDA */
    .main div[data-testid="stMarkdownContainer"] h1,
    .main div[data-testid="stMarkdownContainer"] h2,
    .main div[data-testid="stMarkdownContainer"] h3,
    .main div[data-testid="stMarkdownContainer"] h4 {
        color: #7D1F3A !important;
    }

    /* Texto en info/success/warning boxes - NEGRO */
    .stAlert p {
        color: #000000 !important;
    }
</style>
"""
