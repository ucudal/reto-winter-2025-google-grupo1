# pyright: reportUnknownMemberType=false
import json
import os
from typing import final

from google.cloud import texttospeech
from google.oauth2 import service_account
from pydantic_ai import BinaryContent

from env import env


@final
class TextToSpeechService:
    """Servicio para generar audio usando Google Cloud Text-to-Speech"""

    def __init__(self):
        # Configurar credenciales desde el .env
        self.client = self._create_client()

    def _create_client(self) -> texttospeech.TextToSpeechAsyncClient:
        """Crea el cliente de Text-to-Speech con las credenciales del .env"""
        try:
            environment = env()
            
            # Obtener credenciales del .env
            credentials_json = environment.credentials
            
            if credentials_json:
                # Si las credenciales están en formato dict, usarlas directamente
                if isinstance(credentials_json, dict):
                    credentials = service_account.Credentials.from_service_account_info(
                        credentials_json
                    )
                else:
                    # Si están en formato string JSON, parsearlas
                    credentials_dict = json.loads(credentials_json)
                    credentials = service_account.Credentials.from_service_account_info(
                        credentials_dict
                    )
                
                # Crear cliente con credenciales específicas
                return texttospeech.TextToSpeechAsyncClient(credentials=credentials)
            else:
                # Fallback a credenciales por defecto (ADC)
                return texttospeech.TextToSpeechAsyncClient()
                
        except Exception as e:
            print(f"Warning: Error configurando credenciales específicas: {e}")
            # Fallback a credenciales por defecto
            return texttospeech.TextToSpeechAsyncClient()

    async def generate_audio(
        self, text: str, voice_name: str = "es-ES-Standard-A", language_code: str = "es-ES"
    ) -> BinaryContent:
        """
        Genera un archivo de audio a partir de texto.

        Args:
            text: El texto a convertir en audio (máximo 5000 caracteres)
            voice_name: Nombre de la voz (ej: es-ES-Standard-A, en-US-Standard-C)
            language_code: Código del idioma (ej: es-ES, en-US)

        Returns:
            BinaryContent con el audio generado
        """
        try:
            # Limitar texto para evitar errores
            text = text[:5000]
            
            # Configurar la síntesis de voz
            synthesis_input = texttospeech.SynthesisInput(text=text)

            voice = texttospeech.VoiceSelectionParams(
                language_code=language_code,
                name=voice_name,
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
            )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            # Realizar la síntesis
            response = await self.client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            return BinaryContent(data=response.audio_content, media_type="audio/mpeg")
            
        except Exception as e:
            raise Exception(f"Error generando audio: {str(e)}")

    async def list_available_voices(self, language_code: str = "es-ES") -> list[str]:
        """
        Lista las voces disponibles para un idioma específico.
        
        Args:
            language_code: Código del idioma
            
        Returns:
            Lista de nombres de voces disponibles
        """
        try:
            voices = await self.client.list_voices()
            
            available_voices = [
                voice.name
                for voice in voices.voices
                if voice.language_codes and language_code in voice.language_codes
            ]
            
            return available_voices[:20]  # Limitar a 20 voces
            
        except Exception as e:
            raise Exception(f"Error listando voces: {str(e)}")


# Función de conveniencia para uso directo
async def generate_audio_file(
    text: str, voice: str = "es-ES-Standard-A", language: str = "es-ES"
) -> BinaryContent:
    """
    Función de conveniencia para generar audio.
    
    Args:
        text: Texto a convertir
        voice: Nombre de la voz
        language: Código del idioma
        
    Returns:
        BinaryContent con el audio generado
    """
    service = TextToSpeechService()
    return await service.generate_audio(text, voice, language)
