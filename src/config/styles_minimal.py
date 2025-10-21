"""
CSS MINIMALISTA - Solo elementos custom que NO son nativos de Streamlit
NO tocar selectores de Streamlit - dejar que config.toml maneje los colores
"""

DASHBOARD_CSS = """
<style>
    /* Importar fuente Montserrat */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');

    /* Aplicar fuente SOLO al contenedor principal */
    .stApp {
        font-family: 'Montserrat', sans-serif;
    }

    /* Ocultar elementos de Streamlit que no queremos */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ========== HEADER GUBERNAMENTAL (CUSTOM) ========== */
    .gobierno-header {
        background: linear-gradient(135deg, #7D1F3A 0%, #5D1729 100%);
        padding: 28px 40px;
        border-radius: 0;
        margin: -60px -60px 30px -60px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .gobierno-header h1 {
        color: #FFFFFF !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        padding: 0 !important;
        letter-spacing: -0.5px !important;
    }

    .gobierno-header h3 {
        color: #C4A772 !important;
        font-size: 15px !important;
        font-weight: 400 !important;
        margin: 8px 0 0 0 !important;
        padding: 0 !important;
    }

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

    /* ========== PANEL GUINDA (CUSTOM) ========== */
    .panel-guinda {
        background: linear-gradient(135deg, #7D1F3A 0%, #5D1729 100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(125, 31, 58, 0.2);
    }

    .panel-guinda h4 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        margin: 0 0 15px 0 !important;
    }

    .panel-guinda p {
        color: #FFFFFF !important;
        line-height: 1.8 !important;
        margin: 0 !important;
    }

    .panel-guinda strong {
        color: #C4A772 !important;
    }

    /* ========== CHATBOT CUSTOM ========== */
    .respuesta-asistente {
        background: linear-gradient(135deg, #7D1F3A 0%, #5D1729 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        box-shadow: 0 4px 8px rgba(125, 31, 58, 0.2);
    }

    /* TODO el texto del chatbot debe ser blanco */
    .respuesta-asistente,
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

    .mensaje-usuario {
        background: #f0f0f0;
        padding: 15px 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }

    .mensaje-usuario-texto {
        color: #333333 !important;
    }

    /* ========== SECCIÓN TÍTULOS (CUSTOM) ========== */
    .seccion-titulo {
        color: #2c3e50 !important;
        font-size: 20px !important;
        font-weight: 700 !important;
        margin: 30px 0 16px 0 !important;
        padding-left: 12px !important;
        border-left: 4px solid #7D1F3A !important;
    }

    /* ========== FOOTER (CUSTOM) ========== */
    .footer-gobierno {
        background: white;
        padding: 20px;
        border-radius: 8px;
        margin-top: 40px;
        border-top: 3px solid #7D1F3A;
    }

    .footer-gobierno p {
        color: #6c757d !important;
        font-size: 13px;
        margin: 5px 0;
    }

    /* ========== MEJORAS DE MÉTRICAS ========== */
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

    [data-testid="stMetricValue"] {
        font-size: 42px !important;
        font-weight: 800 !important;
        color: #7D1F3A !important;
    }

    /* ========== BOTONES ========== */
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
</style>
"""
