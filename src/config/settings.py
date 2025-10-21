"""
Configuración general del dashboard
Aquí van todos los valores que se usan en toda la aplicación
"""

# Configuración de la página de Streamlit
PAGE_CONFIG = {
    "page_title": "Sistema de Monitoreo Epidemiológico | SENASICA",
    "page_icon": "🇲🇽",
    "layout": "wide",
    "initial_sidebar_state": "expanded"  # Mostrar sidebar con navegación
}

# Nombre del Google Sheet
SHEET_NAME = "Dashboard_Gusano_Barrenador"

# Tiempo de caché para los datos (en segundos)
CACHE_TTL = 300  # 5 minutos

# Total de municipios en Yucatán
TOTAL_MUNICIPIOS_YUCATAN = 106
