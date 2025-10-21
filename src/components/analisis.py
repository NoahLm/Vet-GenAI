"""
Funciones de análisis y recomendaciones para el chatbot
"""
import pandas as pd


def generar_recomendaciones(df_data, tipo_consulta):
    """
    Genera recomendaciones basadas en el tipo de consulta.

    Args:
        df_data (pd.DataFrame): DataFrame con los datos filtrados
        tipo_consulta (str): Tipo de análisis ('prioridad', 'tendencia', etc.)

    Returns:
        str: Texto en markdown con el análisis y recomendaciones
    """
    municipios_top = df_data.groupby('Municipio_Yucatan')['Casos_Acumulados'].max().sort_values(ascending=False)
    total_casos = int(df_data['Casos_Acumulados'].max())

    if tipo_consulta == "prioridad":
        return _analisis_prioridad(municipios_top, total_casos)

    elif tipo_consulta == "tendencia":
        return _analisis_tendencia(df_data)

    elif tipo_consulta == "apoyos":
        return _informacion_apoyos()

    elif tipo_consulta == "distribucion":
        return _estrategia_distribucion(municipios_top, total_casos)

    elif tipo_consulta == "riesgo":
        return _evaluacion_riesgo(df_data, municipios_top)

    return "Tipo de consulta no reconocido"


def _analisis_prioridad(municipios_top, total_casos):
    """Genera análisis de municipios prioritarios"""
    top_5 = municipios_top.head(5)
    respuesta = """
**MUNICIPIOS QUE REQUIEREN ATENCIÓN PRIORITARIA:**

Los siguientes municipios concentran el mayor número de casos:

"""
    for i, (municipio, casos) in enumerate(top_5.items(), 1):
        porcentaje = (casos / total_casos * 100)
        respuesta += f"{i}. **{municipio}**: {int(casos)} casos ({porcentaje:.1f}% del total)\n"

    respuesta += """

**RECOMENDACIONES:**
- Destinar el 60% de recursos a los 3 municipios principales
- Establecer puntos de verificación móviles en estas zonas
- Priorizar distribución de medicamentos para heridas
- Intensificar liberación de moscas estériles
"""
    return respuesta


def _analisis_tendencia(df_data):
    """Genera análisis de tendencias"""
    df_temporal = df_data.groupby('Fecha_Reporte')['Casos_Semanales'].sum().reset_index()
    casos_semana = int(df_data.groupby('Fecha_Reporte')['Casos_Semanales'].sum().tail(1).values[0]) if len(df_data) > 0 else 0

    if len(df_temporal) >= 4:
        ultimas_4 = df_temporal.tail(4)['Casos_Semanales'].values
        tendencia = "aumentando" if ultimas_4[-1] > ultimas_4[0] else "disminuyendo"
        cambio = ((ultimas_4[-1] - ultimas_4[0]) / ultimas_4[0] * 100) if ultimas_4[0] > 0 else 0
    else:
        tendencia = "estable"
        cambio = 0

    respuesta = f"""
**ANÁLISIS DE TENDENCIA:**

La tendencia de casos está **{tendencia}** con un cambio del **{abs(cambio):.1f}%** en las últimas 4 semanas.

**Casos esta semana:** {casos_semana}

**INTERPRETACIÓN:**
"""
    if tendencia == "aumentando":
        respuesta += """
- ⚠️ **Alerta:** Se requiere intensificar medidas de control
- Aumentar frecuencia de inspecciones en zonas afectadas
- Reforzar campañas de capacitación a ganaderos
- Solicitar moscas estériles adicionales
"""
    else:
        respuesta += """
- ✅ **Positivo:** Las medidas de control están funcionando
- Mantener el nivel actual de recursos
- Continuar con monitoreo regular
- Prepararse para posibles rebrotes
"""
    return respuesta


def _informacion_apoyos():
    """Retorna información sobre apoyos disponibles"""
    return """
**APOYOS DISPONIBLES DE SENASICA:**

**1. Apoyos Inmediatos:**
- ✅ Medicamentos para heridas (gratuitos)
- ✅ Kits de recolección de muestras
- ✅ Atención veterinaria de emergencia (< 24 hrs)

**2. Capacitación:**
- Talleres gratuitos para identificación del gusano
- Técnicas de desinfección y curación de heridas
- Protocolos de bioseguridad

**3. Control Biológico:**
- Liberación de 100 millones de moscas estériles/semana
- Sin costo para los ganaderos

**4. Contacto de Emergencia:**
- 📞 **Teléfono:** 800-751-2100
- 💬 **WhatsApp:** 55-3996-4462

**CÓMO SOLICITAR:**
Llamar inmediatamente al detectar gusaneras en heridas de animales. La atención es en menos de 24 horas.
"""


def _estrategia_distribucion(municipios_top, total_casos):
    """Genera estrategia de distribución de recursos"""
    top_10 = municipios_top.head(10)
    total_top10 = top_10.sum()
    porcentaje_top10 = (total_top10 / total_casos * 100)

    respuesta = f"""
**ESTRATEGIA DE DISTRIBUCIÓN DE RECURSOS:**

Los 10 municipios más afectados concentran el **{porcentaje_top10:.1f}%** de los casos.

**PROPUESTA DE ASIGNACIÓN:**

**Nivel 1 - CRÍTICO (60% de recursos):**
"""
    for municipio, casos in top_10.head(3).items():
        respuesta += f"- {municipio}: {int(casos)} casos\n"

    respuesta += """

**Nivel 2 - ALTO (30% de recursos):**
"""
    for municipio, casos in top_10.iloc[3:7].items():
        respuesta += f"- {municipio}: {int(casos)} casos\n"

    respuesta += """

**Nivel 3 - MODERADO (10% de recursos):**
- Resto de municipios afectados
- Enfoque en prevención y vigilancia

**RECURSOS SUGERIDOS POR NIVEL:**
- **Nivel 1:** Personal veterinario, medicamentos, moscas estériles, inspecciones diarias
- **Nivel 2:** Visitas semanales, medicamentos básicos
- **Nivel 3:** Vigilancia pasiva, capacitaciones mensuales
"""
    return respuesta


def _evaluacion_riesgo(df_data, municipios_top):
    """Genera evaluación de zonas de riesgo"""
    # Calcular municipios con mayor crecimiento
    df_reciente = df_data[df_data['Fecha_Reporte'] >= df_data['Fecha_Reporte'].max() - pd.Timedelta(days=14)]
    crecimiento = df_reciente.groupby('Municipio_Yucatan')['Casos_Semanales'].sum().sort_values(ascending=False)

    respuesta = """
**EVALUACIÓN DE ZONAS DE RIESGO:**

**Municipios con Mayor Actividad (Últimas 2 semanas):**

"""
    for i, (municipio, casos_recientes) in enumerate(crecimiento.head(5).items(), 1):
        casos_totales = municipios_top[municipio]
        respuesta += f"{i}. **{municipio}**: {int(casos_recientes)} casos nuevos (Total: {int(casos_totales)})\n"

    respuesta += """

**FACTORES DE RIESGO:**
- Alta densidad de casos acumulados
- Casos nuevos en las últimas 2 semanas
- Proximidad a municipios afectados

**ACCIONES RECOMENDADAS:**
1. Establecer cercos epidemiológicos
2. Restringir movilización de ganado
3. Intensificar inspecciones en rutas ganaderas
4. Coordinar con municipios vecinos
"""
    return respuesta
