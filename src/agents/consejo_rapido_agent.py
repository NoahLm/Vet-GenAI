# -*- coding: utf-8 -*-
"""
Agente Rápido de Consejos - Gusano Barrenador
Para panel lateral (drawer) - Respuestas rápidas y concisas
"""
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field
from typing import List
import uuid


class PersistentChatMessageHistory(BaseChatMessageHistory, BaseModel):
    """Historial de chat que persiste mensajes por sesión"""
    messages: List[BaseMessage] = Field(default_factory=list)

    def add_message(self, message: BaseMessage) -> None:
        """Agregar mensaje al historial"""
        self.messages.append(message)

    def add_user_message(self, message: str) -> None:
        """Agregar mensaje de usuario"""
        self.add_message(HumanMessage(content=message))

    def add_ai_message(self, message: str) -> None:
        """Agregar mensaje de IA"""
        self.add_message(AIMessage(content=message))

    def clear(self) -> None:
        """Limpiar historial"""
        self.messages = []


class ConsejoRapidoAgent:
    """Agente para consejos rápidos sobre el gusano barrenador"""

    def __init__(self, api_key: str, datos_contexto: str = ""):
        """
        Inicializar agente de consejos rápidos.

        Args:
            api_key: API key de Anthropic
            datos_contexto: Resumen de datos actuales de Yucatán
        """
        self.llm = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            api_key=api_key,
            max_tokens=500,  # Respuestas cortas para drawer
            temperature=0.7
        )

        self.chat_histories = {}
        self.datos_contexto = datos_contexto

        # System prompt para consejos rápidos
        self.system_prompt = f"""Eres un asistente veterinario experto en gusano barrenador, especializado en CONSEJOS RÁPIDOS Y PRÁCTICOS.

CONTEXTO DE DATOS ACTUALES DE YUCATÁN:
{datos_contexto if datos_contexto else "Esperando datos..."}

TU ROL:
- Asistente rápido de SENASICA para ganaderos y técnicos de campo
- Das consejos CONCISOS y ACCIONABLES (máximo 3-4 líneas)
- Respondes rápido, sin información excesiva

TIPOS DE PREGUNTAS QUE RECIBES:
- "¿Qué municipio priorizar hoy?"
- "¿Cómo identificar el gusano?"
- "¿Qué hacer si encuentro un caso?"
- "¿A quién reporto?"
- "¿Cuándo aplicar tratamiento?"

REGLAS ESTRICTAS:
1. Respuestas MÁXIMO 4 líneas
2. Usa emojis (⚠️, ✅, 📍, 📞) para claridad
3. Directo al punto, sin teoría
4. Si necesitan más detalles → recomienda "Pregunta en el Asistente Completo"
5. SIEMPRE incluye datos específicos de Yucatán cuando aplique
6. Termina con un número de contacto si es emergencia

FORMATO DE RESPUESTA:
Emoji + Consejo directo + Dato específico (si aplica)

EJEMPLO:
Usuario: "¿Qué municipio priorizar?"
Tú: "⚠️ **MÉRIDA** tiene 150 casos activos (45% del total).
✅ Prioriza inspecciones en zona norte.
📞 Emergencias: 800-751-2100"

SÉ ULTRA CONCISO. Este es un chat rápido."""

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
        """Actualizar contexto con datos frescos"""
        self.datos_contexto = nuevo_contexto
        self.system_prompt = self.system_prompt.split("CONTEXTO DE DATOS")[0] + \
            f"CONTEXTO DE DATOS ACTUALES DE YUCATÁN:\n{nuevo_contexto}\n\n" + \
            self.system_prompt.split("TU ROL:")[1].split("TU ROL:")[0] + "TU ROL:" + \
            self.system_prompt.split("TU ROL:")[1]

    def obtener_consejo(self, pregunta: str, session_id: str = None) -> str:
        """
        Obtener consejo rápido.

        Args:
            pregunta: Pregunta del usuario
            session_id: ID de sesión (se genera si no existe)

        Returns:
            str: Consejo rápido
        """
        if session_id is None:
            session_id = str(uuid.uuid4())

        try:
            respuesta = self.runnable_chain.invoke(
                {"question": pregunta},
                config={"configurable": {"session_id": session_id}}
            )
            return respuesta
        except Exception as e:
            return f"❌ Error: {str(e)}\n\n💡 Intenta reformular tu pregunta."

    def limpiar_historial(self, session_id: str):
        """Limpiar historial de una sesión"""
        if session_id in self.chat_histories:
            self.chat_histories[session_id].clear()


# Preguntas sugeridas para el drawer
PREGUNTAS_SUGERIDAS_DRAWER = [
    "¿Qué municipio priorizar hoy?",
    "¿Cómo identifico el gusano?",
    "¿Número de emergencias?",
    "Tendencia de esta semana",
    "¿Cuándo aplicar tratamiento?"
]
