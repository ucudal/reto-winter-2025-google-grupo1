# pyright: reportUnknownMemberType=false
from typing import final

from google.cloud import texttospeech
from pydantic_ai import BinaryContent


@final
class TextToSpeechService:
    """Servicio para generar audio usando Google Cloud Text-to-Speech"""

    def __init__(self):
        # TODO: User stored tokens.
        self.client = texttospeech.TextToSpeechAsyncClient()

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
            Ruta del archivo de audio generado
        """
        # Configurar la síntesis de voz
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        # Realizar la síntesis
        response = await self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return BinaryContent(data=response.audio_content, media_type="audio/mpeg")
