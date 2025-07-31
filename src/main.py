import json

from env import env
from google import genai

def main() -> None:
    print(f"{env() = }")

    client = genai.Client(api_key=env().google_cloud_api_key)

    chat = client.chats.create(model="gemini-2.0-flash", config={ "tools": [] })

    for message in ["what the dog doin", "whos a good boi", "summarize what we have been talking about."]:
        print(f"{message = }")
        response = chat.send_message(message)
        print(f"{json.dumps(response.model_dump(mode="json")) = }")
        print(f"{(response.candidates or [])[0].content.parts[0] = }") # pyright: ignore[]


if __name__ == "__main__":
    main()
