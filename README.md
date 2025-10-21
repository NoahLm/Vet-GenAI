# 🇲🇽 Dashboard de Monitoreo Epidemiológico - Gusano Barrenador

Dashboard interactivo para visualizar y analizar datos del brote de gusano barrenador del ganado en Yucatán, México.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)

## 📋 Descripción

Sistema de visualización de datos epidemiológicos diseñado para SENASICA que permite:

- 🗺️ Visualizar casos en mapa interactivo de Yucatán
- 📊 Analizar tendencias temporales
- 📈 Identificar municipios prioritarios
- 🤖 **NUEVO: Asistente AI con Claude** - Análisis inteligente y búsqueda web
- 💡 **NUEVO: Consejo Rápido (Drawer)** - Panel flotante con tips instantáneos
- 🔍 Filtrar por municipio y fecha

## 🏗️ Estructura del Proyecto

```
Vet_GenAI/
├── main.py                          # Archivo principal (ejecuta aquí)
├── requirements.txt                 # Dependencias del proyecto
├── README.md                        # Este archivo
├── .gitignore                       # Archivos ignorados por Git
│
├── venv/                           # Entorno virtual (creado automáticamente)
│
├── src/                            # Código fuente organizado
│   ├── config/                     # Configuraciones
│   │   ├── settings.py             # Configuración general
│   │   ├── styles.py               # Estilos CSS
│   │   └── coordenadas.py          # Coordenadas de municipios
│   │
│   ├── data/                       # Manejo de datos
│   │   └── google_sheets.py        # Conexión a Google Sheets
│   │
│   ├── utils/                      # Funciones auxiliares
│   │   └── preparacion_datos.py    # Preparación de datos
│   │
│   ├── agents/                     # 🆕 Agentes de IA
│   │   ├── __init__.py             # Package initialization
│   │   ├── consejo_rapido_agent.py # Consejos rápidos (drawer)
│   │   └── analisis_completo_agent.py # Análisis profundo con web search
│   │
│   └── components/                 # Componentes visuales
│       ├── graficas.py             # Gráficas de Plotly
│       ├── analisis.py             # Lógica del chatbot estático
│       └── chatbot_ui.py           # 🆕 Interfaz del chatbot AI
│
└── .streamlit/                     # Configuración de Streamlit
    └── secrets.toml                # Credenciales (NO subir a Git)
```

## 🚀 Instalación y Uso

### 1. Activar el entorno virtual

```bash
# En Mac/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar credenciales

Crea el archivo `.streamlit/secrets.toml` con tus credenciales:

```toml
[gcp_service_account]
type = "service_account"
project_id = "tu-proyecto"
private_key_id = "tu-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\ntu-llave-privada\n-----END PRIVATE KEY-----\n"
client_email = "tu-email@tu-proyecto.iam.gserviceaccount.com"
client_id = "tu-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."

# 🆕 Credenciales de Anthropic (Claude AI)
[anthropic]
api_key = "sk-ant-api03-tu-api-key-aqui"
```

**Nota**: Para usar el chatbot AI, necesitas una API key de Anthropic. Obtén una en [console.anthropic.com](https://console.anthropic.com)

### 4. Ejecutar la aplicación

```bash
streamlit run main.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📦 ¿Qué hace cada archivo?

### Configuración (`src/config/`)
- **settings.py**: Valores que se usan en toda la app (nombre del sheet, tiempo de caché, etc.)
- **styles.py**: Todo el CSS del dashboard con el estilo del gobierno
- **coordenadas.py**: Coordenadas (lat/lon) de cada municipio de Yucatán

### Datos (`src/data/`)
- **google_sheets.py**: Se conecta a Google Sheets y trae los datos

### Utilidades (`src/utils/`)
- **preparacion_datos.py**: Transforma los datos para las gráficas (agrupa, calcula métricas, etc.)

### Agentes AI (`src/agents/`) 🆕
- **consejo_rapido_agent.py**: Agente de LangChain para consejos rápidos (drawer)
- **analisis_completo_agent.py**: Agente de LangChain para análisis profundo con web search

### Componentes (`src/components/`)
- **graficas.py**: Crea todas las gráficas (mapa, barras, líneas, cronología)
- **analisis.py**: Genera las recomendaciones estáticas
- **chatbot_ui.py**: 🆕 Interfaz del chatbot AI (drawer y página completa)

### Principal
- **main.py**: Une todo y muestra el dashboard con sistema de pestañas

## 🔧 Configuración Adicional

### Cambiar el nombre del Google Sheet

En `src/config/settings.py`:

```python
SHEET_NAME = "TU_NOMBRE_DE_SHEET"
```

### Cambiar tiempo de caché

En `src/config/settings.py`:

```python
CACHE_TTL = 300  # en segundos (5 minutos)
```

### Agregar municipios nuevos

En `src/config/coordenadas.py`, agregar al diccionario:

```python
COORDENADAS_MUNICIPIOS = {
    'NUEVO_MUNICIPIO': (latitud, longitud),
    # ...resto de municipios
}
```

## 🌐 Desplegar en Internet

### Opción 1: Streamlit Community Cloud (Gratis)

1. Sube tu proyecto a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repositorio
4. Agrega tus secrets (credenciales) en el panel de configuración
5. ¡Listo! Tu app estará en línea

### Opción 2: Otros servicios

- **Render**: https://render.com
- **Railway**: https://railway.app
- **Heroku**: https://heroku.com

## 📚 Dependencias

### Core
- **streamlit**: Framework para crear la app web
- **pandas**: Manejo de datos
- **plotly**: Gráficas interactivas
- **numpy**: Cálculos numéricos

### Google Sheets
- **gspread**: Conexión a Google Sheets
- **google-auth**: Autenticación con Google

### AI / LangChain 🆕
- **anthropic**: API de Claude (Anthropic)
- **langchain**: Framework para aplicaciones con LLMs
- **langchain-anthropic**: Integración de LangChain con Claude
- **langchain-core**: Componentes core de LangChain
- **pydantic**: Validación de datos

## 🤝 Contribuir

Este proyecto fue creado para que sea fácil de entender y modificar. Si encuentras algún error o quieres agregar funcionalidades:

1. Crea un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de uso libre para SENASICA y entidades gubernamentales.

## 📞 Contacto y Soporte

Para emergencias relacionadas con el gusano barrenador:

- **SENASICA**: 800-751-2100
- **WhatsApp**: 55-3996-4462

---

## 🤖 Chatbot AI - Guía Rápida

El dashboard ahora incluye un asistente AI inteligente. Ver **[INSTRUCCIONES_CHATBOT.md](INSTRUCCIONES_CHATBOT.md)** para la guía completa.

### Dos Modos Disponibles:

1. **💡 Asistente Rápido (Drawer)**
   - Panel flotante en la pestaña Dashboard Principal
   - Consejos cortos de máximo 4 líneas
   - Preguntas sugeridas
   - Ideal para consultas rápidas

2. **🔬 Asistente Completo**
   - Pestaña dedicada "🤖 Asistente AI"
   - Análisis profundo y detallado
   - Búsqueda web opcional
   - Comparación con casos internacionales
   - Exportación de conversaciones

### Instalación del Chatbot:

```bash
# Instalar dependencias AI
pip install anthropic langchain langchain-anthropic langchain-core pydantic

# Agregar API key en .streamlit/secrets.toml
# [anthropic]
# api_key = "sk-ant-api03-tu-key-aqui"

# Ejecutar
streamlit run main.py
```

---

**Desarrollado con ❤️ para el monitoreo epidemiológico del gusano barrenador en Yucatán**
