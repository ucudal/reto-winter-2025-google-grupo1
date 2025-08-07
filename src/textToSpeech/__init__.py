"""
Módulo de Text-to-Speech usando Google Cloud Text-to-Speech API.
"""

from .textToSpeech import TextToSpeechService, generate_audio_file

__all__ = ["TextToSpeechService", "generate_audio_file"]