from pydantic_ai import RunContext
from pydantic_ai.toolsets import FunctionToolset

from chat.types import Dependencies
from rag.rag import RAGTool
from rag.types import DocumentFragment, RAGQuery


rag_toolset = FunctionToolset[Dependencies](max_retries=3)

@rag_toolset.tool
async def query_rag(ctx: RunContext[Dependencies], input: RAGQuery) -> list[tuple[DocumentFragment, float]]:
    """
    Query against a local RAG with information about frequent questions towards
    Ithaka. Ithaka has information about a certain university; Universidad
    Católica del Uruguay (UCU).

    Args:
        input: The query and its configuration.
    Returns:
        A list of each relevant match, its nearby context, and its distance.
    """
    print(f"{input = }")
    tool = RAGTool(deps=ctx.deps)
    result = await tool.retrieve_with_vector_search(input)
    print(f"{result = }")
    return result
