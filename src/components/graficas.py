"""
Componentes de gráficas para el dashboard
Cada función crea y retorna una figura de Plotly
"""
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


def crear_mapa_casos(df_mapa):
    """
    Crea el mapa interactivo de casos por municipio.

    Args:
        df_mapa (pd.DataFrame): DataFrame con datos agregados por municipio

    Returns:
        go.Figure: Figura de Plotly con el mapa
    """
    fig = px.scatter_mapbox(
        df_mapa,
        lat='lat',
        lon='lon',
        size='Casos_Acumulados',
        color='Casos_Acumulados',
        hover_name='Municipio_Yucatan',
        hover_data={
            'Casos_Acumulados': ':,',
            'Casos_Semanales': ':,',
            'lat': False,
            'lon': False
        },
        color_continuous_scale=[
            [0, '#FFE5E5'],
            [0.3, '#FF9999'],
            [0.6, '#CC5555'],
            [1, '#7D1F3A']
        ],
        size_max=45,
        zoom=7.3,
        center={'lat': 20.7, 'lon': -89.0},
        mapbox_style='carto-positron',
        height=520,
        labels={
            'Casos_Acumulados': 'Casos Acumulados',
            'Casos_Semanales': 'Casos Semanales'
        }
    )

    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='white',
        font={'size': 12, 'family': 'Montserrat'},
        coloraxis_colorbar=dict(
            title="Casos",
            thickness=18,
            len=0.6,
            bgcolor='white',
            tickfont=dict(size=11)
        )
    )

    return fig


def crear_grafica_barras_municipios(top_municipios):
    """
    Crea gráfica de barras horizontales con los municipios más afectados.

    Args:
        top_municipios (pd.Series): Serie con municipios y casos

    Returns:
        go.Figure: Figura de Plotly con gráfica de barras
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=top_municipios.index,
        x=top_municipios.values,
        orientation='h',
        marker=dict(
            color='#7D1F3A',
            line=dict(color='white', width=1)
        ),
        text=top_municipios.values,
        texttemplate='%{text:,}',
        textposition='outside',
        textfont=dict(size=12, color='#2c3e50', family='Montserrat', weight=600),
        hovertemplate='<b>%{y}</b><br>Casos: %{x:,}<extra></extra>'
    ))

    fig.update_layout(
        height=520,
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'size': 12, 'family': 'Montserrat', 'color': '#2c3e50'},
        xaxis=dict(
            title='Casos Acumulados',
            gridcolor='#f0f0f0',
            showgrid=True,
            zeroline=False,
            tickfont=dict(size=11)
        ),
        yaxis=dict(
            title='',
            categoryorder='total ascending',
            tickfont=dict(size=11, color='#333333')
        ),
        margin=dict(l=10, r=70, t=10, b=50)
    )

    return fig


def crear_grafica_casos_semanales(df_tiempo):
    """
    Crea gráfica de casos semanales con línea de tendencia.

    Args:
        df_tiempo (pd.DataFrame): DataFrame con casos por fecha

    Returns:
        go.Figure: Figura de Plotly con gráfica de línea
    """
    fig = go.Figure()

    # Barras de casos semanales
    fig.add_trace(go.Bar(
        x=df_tiempo['Fecha_Reporte'],
        y=df_tiempo['Casos_Semanales'],
        name='Casos Semanales',
        marker_color='#CC5555',
        opacity=0.8,
        hovertemplate='<b>Semana del %{x|%d/%m/%Y}</b><br>Casos: %{y:,}<extra></extra>'
    ))

    # Línea de tendencia
    if len(df_tiempo) > 2:
        x_numeric = list(range(len(df_tiempo)))
        y_values = df_tiempo['Casos_Semanales'].values
        z = np.polyfit(x_numeric, y_values, min(2, len(df_tiempo)-1))
        p = np.poly1d(z)
        tendencia = p(x_numeric)

        fig.add_trace(go.Scatter(
            x=df_tiempo['Fecha_Reporte'],
            y=tendencia,
            name='Línea de Tendencia',
            line=dict(color='#7D1F3A', width=3, dash='dash'),
            mode='lines',
            hovertemplate='<b>Tendencia</b><extra></extra>'
        ))

    fig.update_layout(
        height=380,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'size': 11, 'family': 'Montserrat', 'color': '#2c3e50'},
        xaxis=dict(
            title='',
            gridcolor='#f0f0f0',
            showgrid=True,
            tickformat='%d/%m'
        ),
        yaxis=dict(
            title='Casos Semanales',
            gridcolor='#f0f0f0',
            showgrid=True,
            rangemode='tozero'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255,255,255,0.9)'
        ),
        margin=dict(l=50, r=20, t=30, b=50),
        hovermode='x unified'
    )

    return fig


def crear_cronologia_propagacion(primer_caso_municipio):
    """
    Crea gráfica de cronología de propagación por municipio.

    Args:
        primer_caso_municipio (pd.DataFrame): DataFrame con primer caso por municipio

    Returns:
        go.Figure: Figura de Plotly con cronología
    """
    # Agrupar por fecha para contar municipios por día
    municipios_por_fecha = primer_caso_municipio.groupby('Fecha_Reporte').size().reset_index(name='Cantidad')

    fig = go.Figure()

    # Añadir líneas verticales para cada fecha
    for _, row in municipios_por_fecha.iterrows():
        municipios_esa_fecha = primer_caso_municipio[primer_caso_municipio['Fecha_Reporte'] == row['Fecha_Reporte']]
        municipios_nombres = ', '.join(municipios_esa_fecha['Municipio_Yucatan'].tolist())

        fig.add_trace(go.Scatter(
            x=[row['Fecha_Reporte'], row['Fecha_Reporte']],
            y=[0, row['Cantidad']],
            mode='lines',
            line=dict(color='#CC5555', width=2),
            showlegend=False,
            hoverinfo='skip'
        ))

        # Punto en la parte superior
        fig.add_trace(go.Scatter(
            x=[row['Fecha_Reporte']],
            y=[row['Cantidad']],
            mode='markers+text',
            marker=dict(
                size=12 + (row['Cantidad'] * 2),
                color='#7D1F3A',
                line=dict(color='white', width=2)
            ),
            text=[f"{row['Cantidad']}" if row['Cantidad'] > 1 else ""],
            textposition='top center',
            textfont=dict(color='#7D1F3A', size=10, family='Montserrat', weight=600),
            name='',
            showlegend=False,
            customdata=[[municipios_nombres]],
            hovertemplate='<b>%{x|%d/%m/%Y}</b><br>Municipios nuevos: ' + str(row['Cantidad']) + '<br><b>Municipios:</b> %{customdata[0]}<extra></extra>'
        ))

    # Anotación para el primer municipio
    primer_municipio = primer_caso_municipio.iloc[0]
    fig.add_annotation(
        x=primer_municipio['Fecha_Reporte'],
        y=1,
        text=f"<b>INICIO</b><br>{primer_municipio['Municipio_Yucatan']}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=2,
        arrowcolor='#00A86B',
        font=dict(size=10, color='#00A86B', family='Montserrat', weight='bold'),
        bgcolor='rgba(255,255,255,0.95)',
        bordercolor='#00A86B',
        borderwidth=2,
        borderpad=6,
        ax=0,
        ay=-40
    )

    fig.update_layout(
        height=400,
        paper_bgcolor='white',
        plot_bgcolor='white',
        font={'size': 11, 'family': 'Montserrat', 'color': '#2c3e50'},
        xaxis=dict(
            title='Fecha de Primer Caso',
            gridcolor='#f0f0f0',
            showgrid=True,
            tickformat='%d/%m/%Y',
            dtick='M1'
        ),
        yaxis=dict(
            title='Cantidad de Municipios Nuevos',
            gridcolor='#f0f0f0',
            showgrid=True,
            rangemode='tozero'
        ),
        margin=dict(l=60, r=20, t=80, b=60),
        hovermode='closest'
    )

    return fig
