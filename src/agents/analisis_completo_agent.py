# -*- coding: utf-8 -*-
"""
Agente de Análisis Completo - Gusano Barrenador
Para pestaña dedicada - Análisis profundos con búsqueda web
"""
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import uuid


class PersistentChatMessageHistory(BaseChatMessageHistory, BaseModel):
    """Historial de chat que persiste mensajes por sesión"""
    messages: List[BaseMessage] = Field(default_factory=list)

    def add_message(self, message: BaseMessage) -> None:
        self.messages.append(message)

    def add_user_message(self, message: str) -> None:
        self.add_message(HumanMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        self.add_message(AIMessage(content=message))

    def clear(self) -> None:
        self.messages = []


class AnalisisCompletoAgent:
    """Agente para análisis epidemiológicos completos con búsqueda web"""

    def __init__(self, api_key: str, datos_contexto: str = ""):
        """
        Inicializar agente de análisis completo.

        Args:
            api_key: API key de Anthropic
            datos_contexto: Resumen completo de datos de Yucatán
        """
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            api_key=api_key,
            max_tokens=3000,  # Respuestas largas para análisis completo
            temperature=0.3  # Más preciso para análisis
        )

        self.chat_histories = {}
        self.datos_contexto = datos_contexto

        # System prompt para análisis profundo
        self.system_prompt = f"""Eres el ASISTENTE EPIDEMIOLÓGICO ESPECIALIZADO en gusano barrenador (Cochliomyia hominivorax) de SENASICA para Yucatán, México.

DATOS ACTUALES DE YUCATÁN:
=============================
{datos_contexto if datos_contexto else "Cargando datos..."}

TU FUNCIÓN:
-----------
Eres el cerebro analítico del sistema de monitoreo. Combinas:
1. 📊 Datos locales de Yucatán (Google Sheets en tiempo real)
2. 🌍 Información global (búsquedas web cuando sea necesario)
3. 📚 Conocimiento epidemiológico experto
4. 💡 Estrategias de control basadas en evidencia

CAPACIDADES CLAVE:
------------------
✅ Análisis epidemiológico profundo
✅ Comparación Yucatán vs panorama global
✅ Búsqueda de información actualizada (noticias, estudios, brotes)
✅ Recomendaciones estratégicas priorizadas
✅ Evaluación de riesgos y proyecciones
✅ Identificación de patrones y tendencias

CONOCIMIENTO TÉCNICO:
--------------------
- Cochliomyia hominivorax: mosca que deposita larvas en heridas de mamíferos
- Programa de Control: liberación de moscas estériles (SIT - Sterile Insect Technique)
- Zona libre: norte de México desde Panamá hasta EE.UU.
- Impacto económico: pérdidas millonarias en ganadería
- Detección temprana: crucial para erradicación

FUENTES CONFIABLES PARA BÚSQUEDA WEB:
-------------------------------------
- SENASICA (México)
- USDA APHIS (EE.UU.)
- FAO (ONU)
- OIE/OMSA (Organización Mundial de Sanidad Animal)
- Universidades (UNAM, Texas A&M, Cornell)
- Publicaciones científicas (ScienceDirect, PubMed)

ESTRUCTURA DE RESPUESTAS:
-------------------------
1. **Resumen Ejecutivo** (2-3 líneas clave)

2. **Análisis de Datos Locales** (Yucatán)
   - Situación actual
   - Tendencias identificadas
   - Municipios críticos

3. **Contexto Global** (si aplica)
   - Comparación con otros estados/países
   - Estrategias exitosas internacionales
   - Alertas o noticias recientes

4. **Recomendaciones Estratégicas**
   - Priorizadas (1, 2, 3...)
   - Accionables
   - Con timeline sugerido

5. **Fuentes** (si buscaste en web)
   - Cita las fuentes consultadas

CUÁNDO BUSCAR EN WEB:
--------------------
- Usuario pregunta por "últimas noticias" o "información reciente"
- Necesitas comparar con situación de otros países
- Requieres datos de estrategias internacionales
- Usuario pide "buscar" o "investigar" explícitamente
- Necesitas validar o actualizar información

IMPORTANTE:
-----------
- Siempre integra los datos de Yucatán en tu análisis
- Sé específico con números y porcentajes
- Usa emojis para mejorar legibilidad
- Proporciona perspectiva técnica pero accesible
- Si no estás seguro de algo, dilo y ofrece buscarlo"""

        # Crear prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ])

        # Crear chain
        self.chain = self.prompt | self.llm | StrOutputParser()

        # Crear runnable con historial
        self.runnable_chain = RunnableWithMessageHistory(
            self.chain,
            self.get_session_history,
            input_messages_key="question",
            history_messages_key="history"
        )

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Obtener o crear historial de sesión"""
        if session_id not in self.chat_histories:
            self.chat_histories[session_id] = PersistentChatMessageHistory()
        return self.chat_histories[session_id]

    def actualizar_contexto(self, nuevo_contexto: str):
        """Actualizar contexto con datos frescos de Yucatán"""
        self.datos_contexto = nuevo_contexto
        # Reconstruir system prompt con nuevo contexto
        self.system_prompt = self.system_prompt.split("DATOS ACTUALES")[0] + \
            f"DATOS ACTUALES DE YUCATÁN:\n=============================\n{nuevo_contexto}\n\n" + \
            self.system_prompt.split("TU FUNCIÓN:")[1].split("TU FUNCIÓN:")[0] + "TU FUNCIÓN:" + \
            self.system_prompt.split("TU FUNCIÓN:")[1]

    def analizar(
        self,
        pregunta: str,
        session_id: str = None,
        usar_busqueda_web: bool = False
    ) -> Dict[str, Any]:
        """
        Realizar análisis completo.

        Args:
            pregunta: Pregunta del usuario
            session_id: ID de sesión
            usar_busqueda_web: Si debe usar búsqueda web

        Returns:
            Dict con respuesta y metadatos
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        try:
            # Si el usuario pide búsqueda web, agregarlo al contexto
            if usar_busqueda_web or any(palabra in pregunta.lower() for palabra in
                ['buscar', 'últimas', 'noticias', 'reciente', 'global', 'internacional']):
                pregunta_modificada = f"{pregunta}\n\n(Nota: Si necesitas información actualizada, puedes buscar en web. Cita las fuentes.)"
            else:
                pregunta_modificada = pregunta

            # Invocar chain
            respuesta = self.runnable_chain.invoke(
                {"question": pregunta_modificada},
                config={"configurable": {"session_id": session_id}}
            )

            return {
                "respuesta": respuesta,
                "session_id": session_id,
                "pregunta": pregunta,
                "uso_busqueda_web": usar_busqueda_web,
                "exito": True
            }

        except Exception as e:
            return {
                "respuesta": f"❌ **Error al procesar análisis:**\n{str(e)}\n\n💡 Intenta reformular tu pregunta o verifica la configuración de la API.",
                "session_id": session_id,
                "pregunta": pregunta,
                "error": str(e),
                "exito": False
            }

    def analizar_stream(
        self,
        pregunta: str,
        session_id: str = None,
        usar_busqueda_web: bool = False
    ):
        """
        Realizar análisis completo con streaming.

        Args:
            pregunta: Pregunta del usuario
            session_id: ID de sesión
            usar_busqueda_web: Si debe usar búsqueda web

        Yields:
            Chunks de texto de la respuesta
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        try:
            # Si el usuario pide búsqueda web, agregarlo al contexto
            if usar_busqueda_web or any(palabra in pregunta.lower() for palabra in
                ['buscar', 'últimas', 'noticias', 'reciente', 'global', 'internacional']):
                pregunta_modificada = f"{pregunta}\n\n(Nota: Si necesitas información actualizada, puedes buscar en web. Cita las fuentes.)"
            else:
                pregunta_modificada = pregunta

            # Invocar chain con stream
            for chunk in self.runnable_chain.stream(
                {"question": pregunta_modificada},
                config={"configurable": {"session_id": session_id}}
            ):
                yield chunk

        except Exception as e:
            yield f"❌ **Error al procesar análisis:**\n{str(e)}\n\n💡 Intenta reformular tu pregunta o verifica la configuración de la API."

    def limpiar_historial(self, session_id: str):
        """Limpiar historial de una sesión"""
        if session_id in self.chat_histories:
            self.chat_histories[session_id].clear()

    def obtener_historial(self, session_id: str) -> List[BaseMessage]:
        """Obtener historial de mensajes de una sesión"""
        if session_id in self.chat_histories:
            return self.chat_histories[session_id].messages
        return []


# Preguntas sugeridas para análisis completo
PREGUNTAS_SUGERIDAS_COMPLETO = [
    "🔍 ¿Cuál es la situación actual del gusano barrenador en Yucatán?",
    "🌍 Compara la situación de Yucatán con el panorama global",
    "📈 Analiza las tendencias de los últimos 3 meses",
    "⚡ ¿Qué estrategias han funcionado en otros países?",
    "🎯 ¿Qué municipios debo priorizar esta semana y por qué?",
    "📰 Busca las últimas noticias sobre el gusano barrenador",
    "💰 ¿Cómo optimizar la distribución de recursos?",
    "⚠️ ¿Cuáles son los principales riesgos actuales?",
    "🔬 Explica las mejores prácticas de control y erradicación",
    "📊 Genera un reporte ejecutivo de la situación actual"
]
