# pyright: reportUnknownMemberType=false
from pathlib import Path
from typing import final

from google.cloud import texttospeech
from pydantic_ai import BinaryContent


@final
class TextToSpeechService:
    """Servicio para generar audio usando Google Cloud Text-to-Speech"""

    def __init__(self, audio_dir: str = "static/audio"):
        self.client = texttospeech.TextToSpeechClient()
        self.audio_dir = Path(audio_dir)
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    def generate_audio(
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
        # Limitar el texto para evitar archivos muy largos
        text = text[:5000]

        # Configurar la síntesis de voz
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        # Realizar la síntesis
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return BinaryContent(data=response.audio_content, media_type="audio/mpeg")

    def list_voices(self, language_code: str = "es-ES") -> list[str]:
        """
        Lista las voces disponibles para un idioma específico.

        Args:
            language_code: Código del idioma

        Returns:
            Lista de nombres de voces disponibles
        """
        voices = self.client.list_voices(language_code=language_code)
        return [voice.name for voice in voices.voices][:20]
