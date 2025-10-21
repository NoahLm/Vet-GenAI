"""
Estilos CSS del dashboard
Todo el CSS está aquí separado para mantenerlo organizado
"""

# CSS completo del dashboard con estilo gobierno
DASHBOARD_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');

    * {
        font-family: 'Montserrat', sans-serif;
    }

    .stApp {
        background-color: #f5f5f5;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Header Gubernamental */
    .gobierno-header {
        background: linear-gradient(135deg, #7D1F3A 0%, #5D1729 100%);
        padding: 28px 40px;
        border-radius: 0;
        margin: -60px -60px 30px -60px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .gobierno-header h1 {
        color: white !important;
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

    /* Tarjetas de Métricas - Estilo Gobierno */
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

    [data-testid="stMetricLabel"] {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #6c757d !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        margin-bottom: 8px !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 42px !important;
        font-weight: 800 !important;
        color: #7D1F3A !important;
        line-height: 1 !important;
    }

    /* Secciones */
    .seccion-titulo {
        color: #2c3e50;
        font-size: 20px;
        font-weight: 700;
        margin: 30px 0 16px 0;
        padding-left: 12px;
        border-left: 4px solid #7D1F3A;
    }

    /* Contenedores de gráficos */
    .grafico-container {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    /* Botones */
    .stButton button {
        background: linear-gradient(135deg, #7D1F3A 0%, #5D1729 100%);
        color: white;
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

    /* Expander de filtros */
    .streamlit-expanderHeader {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        font-weight: 600;
        color: #2c3e50;
    }

    /* Footer gubernamental */
    .footer-gobierno {
        background: white;
        padding: 20px;
        border-radius: 8px;
        margin-top: 40px;
        border-top: 3px solid #7D1F3A;
    }

    .footer-gobierno p {
        color: #6c757d;
        font-size: 13px;
        margin: 5px 0;
    }

    /* Tablas */
    .dataframe {
        font-size: 13px !important;
    }

    .dataframe thead tr th {
        background-color: #7D1F3A !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 12px 8px !important;
    }

    /* Subtítulos de gráficos */
    h3 {
        color: #2c3e50 !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }
</style>
"""
