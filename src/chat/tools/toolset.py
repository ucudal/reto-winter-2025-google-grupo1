from pydantic_ai import RunContext
from pydantic_ai.toolsets import CombinedToolset, FunctionToolset

from chat.types import Dependencies
from forms.toolset import form_tools
from rag.toolset import rag_toolset
from textToSpeech.textToSpeech import TextToSpeechService


_local_funcs = FunctionToolset[Dependencies](max_retries=3)


# Tools that start with dev_ are filtered in prod.
@_local_funcs.tool
def dev_debug_dependencies(ctx: RunContext[Dependencies], input: str) -> Dependencies:
    """
    This is an example function call to show developers.
    Show it when asked for the test function or anything like that, and tell
    them about the result of the call. If someone looks like a token,
    don't leak it, just say that you can see it, and maybe say some minimal
    information about it (it starts with 'a').

    Parameters:
        :input: An arbitrary string. Put whatever there.

    Returns:
        The dependencies object.
    """

    print(f"{input = }")
    # Avoid printing sensitive data - only print safe fields
    print(f"Environment: {ctx.deps.env.environment}")

    return ctx.deps


@_local_funcs.tool
def generate_audio_response(ctx: RunContext[Dependencies], text: str, voice: str = "es-ES-Standard-A", language_code: str = "es-ES") -> str:
    """
    Genera un archivo de audio a partir de texto usando Google Cloud Text-to-Speech.
    
    Parameters:
        :text: El texto que se convertirá a audio (máximo 5000 caracteres)
        :voice: Nombre de la voz (ej: es-ES-Standard-A, en-US-Standard-C, es-ES-Neural2-A)
        :language_code: Código del idioma (ej: es-ES, en-US, fr-FR)
    
    Returns:
        Información sobre el archivo de audio generado
    """
    try:
        tts_service = TextToSpeechService()
        filepath = tts_service.generate_audio(text, voice, language_code)
        
        # Extraer solo el nombre del archivo para la respuesta
        filename = filepath.split("/")[-1].split("\\")[-1]
        
        return f"🎵 Audio generado exitosamente: {filename}\n📁 Ubicación: {filepath}\n🌐 Puedes acceder al audio en la interfaz web."
        
    except ImportError:
        return "❌ Error: Google Cloud Text-to-Speech no está instalado. Instala con: pip install google-cloud-texttospeech"
    except Exception as e:
        return f"❌ Error generando audio: {str(e)}"


@_local_funcs.tool
def list_available_voices(ctx: RunContext[Dependencies], language_code: str = "es-ES") -> str:
    """
    Lista las voces disponibles para un idioma específico en Google Cloud Text-to-Speech.
    
    Parameters:
        :language_code: Código del idioma (ej: es-ES, en-US, fr-FR, pt-BR)
    
    Returns:
        Lista de voces disponibles para el idioma especificado
    """
    try:
        tts_service = TextToSpeechService()
        voices = tts_service.list_voices(language_code)
        
        if voices:
            voices_text = "\n".join([f"• {voice}" for voice in voices])
            return f"🎤 Voces disponibles para {language_code}:\n{voices_text}"
        else:
            return f"❌ No se encontraron voces para el idioma {language_code}"
            
    except ImportError:
        return "❌ Error: Google Cloud Text-to-Speech no está instalado."
    except Exception as e:
        return f"❌ Error listando voces: {str(e)}"


# If you make other toolsets, add them here.
# This is what is loaded into the bot.
main_toolset = CombinedToolset[Dependencies]([_local_funcs, form_tools, rag_toolset]).filtered(
    lambda ctx, tool: ctx.deps.env.environment == "dev" or not tool.name.startswith("dev_")
)
