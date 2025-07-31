from collections.abc import Sequence
from functools import cache
from google import genai
from google.genai.types import Part
from env import env

@cache
def get_client(api_key: str):
    """
    Return a cached Gemini AI client instance initialized with the specified API key.
    """
    return genai.Client(api_key=api_key)

@cache
def get_chat(id: str):
    """
    Return a cached Gemini chat session using the Google Cloud API key and the "gemini-2.0-flash" model.
    
    Parameters:
        id (str): Identifier for the chat session.
    
    Returns:
        A chat session object for interacting with the Gemini API.
    """
    return get_client(env().google_cloud_api_key).chats.create(model="gemini-2.0-flash")

def answer(message: Sequence[Part]) -> list[Part]:
    """
    Send a message to the Gemini chat session and return the response parts.
    
    If the response does not contain valid candidates or content, returns a single part with an error message in Spanish.
    
    Parameters:
        message (Sequence[Part]): The message parts to send to the chat session.
    
    Returns:
        list[Part]: The parts from the first candidate's content in the response, or an error part if the response is invalid.
    """
    chat = get_chat("test")

    response = chat.send_message(list(message))

    if (
        not response.candidates
        or not response.candidates[0].content
        or not response.candidates[0].content.parts
    ):
        return [Part.from_text(text="Ocurrió un error")]

    return response.candidates[0].content.parts


def get_history() -> list[Part]: """
Retrieve the message history from the chat session.

Returns:
    list[Part]: The list of message parts representing the chat history.
"""
...
