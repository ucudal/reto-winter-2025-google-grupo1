# pyright: reportUnknownMemberType=false
from typing import final

from google.cloud import texttospeech
from pydantic_ai import BinaryContent

from env import Environment


@final
class TextToSpeechService:
    def __init__(self, env: Environment):
        self._env = env
        self.client = self._create_client()

    def _create_client(self) -> texttospeech.TextToSpeechAsyncClient:
        return texttospeech.TextToSpeechAsyncClient(credentials=self._env.credentials)

    async def generate_audio(
        self, text: str, voice_name: str = "es-ES-Standard-A", language_code: str = "es-ES"
    ) -> BinaryContent:
        text = text[:5000]

        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = await self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return BinaryContent(data=response.audio_content, media_type="audio/mpeg")

    async def list_available_voices(self, language_code: str = "es-ES") -> list[str]:
        voices = await self.client.list_voices()

        available_voices = [
            voice.name
            for voice in voices.voices
            if voice.language_codes and language_code in voice.language_codes
        ]

        return available_voices[:20]
