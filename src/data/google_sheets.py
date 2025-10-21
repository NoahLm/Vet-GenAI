"""
Funciones para conectarse y cargar datos desde Google Sheets
"""
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

from ..config.settings import SHEET_NAME, CACHE_TTL


@st.cache_data(ttl=CACHE_TTL)
def cargar_datos_desde_sheets():
    """
    Carga los datos desde Google Sheets y los convierte a DataFrame.
    Los datos se cachean por 5 minutos para mejorar el rendimiento.

    Returns:
        pd.DataFrame: DataFrame con los datos del gusano barrenador
    """
    try:
        # Obtener credenciales desde secrets de Streamlit
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets.readonly",
                "https://www.googleapis.com/auth/drive.readonly"
            ]
        )

        # Conectar a Google Sheets
        gc = gspread.authorize(credentials)
        sheet = gc.open(SHEET_NAME).sheet1

        # Obtener todos los datos
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        # Convertir fecha a datetime
        df['Fecha_Reporte'] = pd.to_datetime(df['Fecha_Reporte'])

        return df

    except Exception as e:
        st.error(f"❌ Error al conectar con Google Sheets: {e}")
        return pd.DataFrame()


def aplicar_filtros(df, municipio_seleccionado, fecha_inicio, fecha_fin):
    """
    Aplica filtros de municipio y fecha al DataFrame.

    Args:
        df (pd.DataFrame): DataFrame original
        municipio_seleccionado (list): Lista de municipios seleccionados
        fecha_inicio (date): Fecha de inicio del filtro
        fecha_fin (date): Fecha fin del filtro

    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    df_filtrado = df.copy()

    # Filtrar por municipio
    if 'Todos' not in municipio_seleccionado and municipio_seleccionado:
        df_filtrado = df_filtrado[df_filtrado['Municipio_Yucatan'].isin(municipio_seleccionado)]

    # Filtrar por fecha
    df_filtrado = df_filtrado[
        (df_filtrado['Fecha_Reporte'].dt.date >= fecha_inicio) &
        (df_filtrado['Fecha_Reporte'].dt.date <= fecha_fin)
    ]

    return df_filtrado
