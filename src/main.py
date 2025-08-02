# Rabbit, you son of a lovely lady, this file is for goofing around and testing
# stuff. Please, for all that is holy, do not bother me in prs with this file
# or duplicated functionality because of the mess that this file is.

import json
from env import env
from google import genai


def main() -> None:
    print(f"{env() = }")

    client = genai.Client(api_key=env().google_cloud_api_key)

    chat = client.chats.create(model="gemini-2.0-flash")

    for message in [
        "what the dog doin",
        "whos a good boi",
        "summarize what we have been talking about.",
    ]:
        print(f"{message = }")
        response = chat.send_message(message)
        print(f"{(response.candidates or [])[0].content.parts[0] = }")  # pyright: ignore[reportOptionalSubscript, reportOptionalMemberAccess]

    client = genai.Client(api_key=env().google_cloud_api_key)

    chat = client.chats.create(model="gemini-2.0-flash", config={"tools": []})

    for message in [
        "what the dog doin",
        "whos a good boi",
        "summarize what we have been talking about.",
    ]:
        print(f"{message = }")
        response = chat.send_message(message)
        print(f"{json.dumps(response.model_dump(mode="json")) = }")
        print(f"{(response.candidates or [])[0].content = }")


if __name__ == "__main__":
    main()
