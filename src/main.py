# Rabbit, you son of a lovely lady, this file is for goofing around and testing
# stuff. Please, for all that is holy, do not bother me in prs with this file
# or duplicated functionality because of the mess that this file is.
import asyncio
from google import genai
from google.cloud import bigquery
from chat.types import Dependencies
from env import env
from rag.rag import RAGTool
from rag.types import RAGQuery


async def main() -> None:
    tool = RAGTool(
        deps=Dependencies(
            env=env(),
            bq_client=bigquery.Client(project=env().project_id),
            google_client=genai.Client(api_key=env().google_cloud_api_key).aio,
        )
    )

    result = await tool.retrieve_with_vector_search(
        RAGQuery(query="Qué cursos electivos puedo hacer en ithaka?")
    )

    print(f"{result = }")


if __name__ == "__main__":
    asyncio.run(main())
