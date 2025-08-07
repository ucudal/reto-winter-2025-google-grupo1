import os
import uuid
from pathlib import Path
from typing import Optional

from google.cloud import texttospeech


class TextToSpeechService:
    """Servicio para generar audio usando Google Cloud Text-to-Speech"""
    
    def __init__(self, audio_dir: str = "static/audio"):
        self.client = texttospeech.TextToSpeechClient()
        self.audio_dir = Path(audio_dir)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_audio(
        self, 
        text: str, 
        voice_name: str = "es-ES-Standard-A", 
        language_code: str = "es-ES"
    ) -> str:
        """
        Genera un archivo de audio a partir de texto.
        
        Args:
            text: El texto a convertir en audio (máximo 5000 caracteres)
            voice_name: Nombre de la voz (ej: es-ES-Standard-A, en-US-Standard-C)
            language_code: Código del idioma (ej: es-ES, en-US)
            
        Returns:
            Ruta del archivo de audio generado
            
        Raises:
            Exception: Si hay un error en la generación del audio
        """
        try:
            # Limitar el texto para evitar archivos muy largos
            text = text[:5000]
            
            # Generar nombre único para el archivo
            filename = f"response_{uuid.uuid4().hex[:8]}.mp3"
            filepath = self.audio_dir / filename
            
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
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Guardar el archivo de audio
            with open(filepath, "wb") as out:
                out.write(response.audio_content)
            
            return str(filepath)
            
        except Exception as e:
            raise Exception(f"Error generando audio: {str(e)}")
    
    def list_voices(self, language_code: str = "es-ES") -> list[str]:
        """
        Lista las voces disponibles para un idioma específico.
        
        Args:
            language_code: Código del idioma
            
        Returns:
            Lista de nombres de voces disponibles
        """
        try:
            voices = self.client.list_voices()
            
            available_voices = [
                voice.name
                for voice in voices.voices
                if voice.language_codes and language_code in voice.language_codes
            ]
            
            return available_voices[:20]  # Limitar a 20 voces
            
        except Exception as e:
            raise Exception(f"Error listando voces: {str(e)}")


# Función de conveniencia para uso directo
def generate_audio_file(text: str, voice: str = "es-ES-Standard-A", language: str = "es-ES") -> str:
    """
    Función de conveniencia para generar audio.
    
    Args:
        text: Texto a convertir
        voice: Nombre de la voz
        language: Código del idioma
        
    Returns:
        Ruta del archivo generado
    """
    service = TextToSpeechService()
    return service.generate_audio(text, voice, language)