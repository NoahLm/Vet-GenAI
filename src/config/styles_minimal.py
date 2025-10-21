"""
CSS SUPER SIMPLE - SOLO header custom, TODO lo demás es nativo de Streamlit
"""

DASHBOARD_CSS = """
<style>
    /* Importar fuente */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700;800&display=swap');

    .stApp {
        font-family: 'Montserrat', sans-serif;
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ========== SOLO EL HEADER CUSTOM ========== */
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
    }

    .gobierno-header h3 {
        color: #C4A772 !important;
        font-size: 15px !important;
        font-weight: 400 !important;
        margin: 8px 0 0 0 !important;
    }

    .badge-gobierno {
        background: #C4A772;
        color: #7D1F3A;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        margin-left: 15px;
    }
</style>
"""
