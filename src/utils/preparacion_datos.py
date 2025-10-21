"""
Funciones para preparar y transformar datos para las visualizaciones
"""
import pandas as pd
from ..config.coordenadas import obtener_coordenadas


def agregar_coordenadas(df):
    """
    Agrega columnas de latitud y longitud al DataFrame basándose
    en el municipio.

    Args:
        df (pd.DataFrame): DataFrame con columna 'Municipio_Yucatan'

    Returns:
        pd.DataFrame: DataFrame con columnas 'lat' y 'lon' agregadas
    """
    df_con_coords = df.copy()
    df_con_coords['lat'] = df_con_coords['Municipio_Yucatan'].apply(
        lambda x: obtener_coordenadas(x)[0]
    )
    df_con_coords['lon'] = df_con_coords['Municipio_Yucatan'].apply(
        lambda x: obtener_coordenadas(x)[1]
    )
    return df_con_coords


def preparar_datos_mapa(df):
    """
    Prepara los datos para el mapa, agrupando por municipio.

    Args:
        df (pd.DataFrame): DataFrame filtrado con coordenadas

    Returns:
        pd.DataFrame: DataFrame agrupado listo para el mapa
    """
    df_mapa = df.groupby('Municipio_Yucatan').agg({
        'Casos_Acumulados': 'max',
        'Casos_Semanales': 'sum',
        'lat': 'first',
        'lon': 'first'
    }).reset_index()

    return df_mapa


def calcular_metricas_generales(df):
    """
    Calcula las métricas principales del dashboard.

    Args:
        df (pd.DataFrame): DataFrame filtrado

    Returns:
        dict: Diccionario con las métricas calculadas
    """
    return {
        'total_municipios': df['Municipio_Yucatan'].nunique(),
        'total_casos': int(df['Casos_Acumulados'].max()),
        'casos_semana': int(df['Casos_Semanales'].sum()),
        'ultima_fecha': df['Fecha_Reporte'].max().strftime('%d-%m-%Y')
    }


def obtener_top_municipios(df, n=10):
    """
    Obtiene los municipios con más casos acumulados.

    Args:
        df (pd.DataFrame): DataFrame filtrado
        n (int): Número de municipios a retornar

    Returns:
        pd.Series: Serie con los top municipios y sus casos
    """
    return df.groupby('Municipio_Yucatan')['Casos_Acumulados'].max().sort_values(ascending=False).head(n)


def preparar_datos_temporales(df):
    """
    Prepara los datos agrupados por fecha para gráficas temporales.

    Args:
        df (pd.DataFrame): DataFrame filtrado

    Returns:
        pd.DataFrame: DataFrame agrupado por fecha
    """
    return df.groupby('Fecha_Reporte')['Casos_Semanales'].sum().reset_index()


def preparar_cronologia_primer_caso(df):
    """
    Prepara datos de cronología del primer caso por municipio.

    Args:
        df (pd.DataFrame): DataFrame filtrado

    Returns:
        pd.DataFrame: DataFrame con primer caso por municipio
    """
    primer_caso = df.sort_values('Fecha_Reporte').groupby('Municipio_Yucatan').first().reset_index()
    primer_caso = primer_caso[['Municipio_Yucatan', 'Fecha_Reporte', 'Casos_Semanales']].copy()
    return primer_caso.sort_values('Fecha_Reporte')
