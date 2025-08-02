from pydantic_ai import RunContext
from pydantic_ai.toolsets import CombinedToolset, FunctionToolset

from chat.types import Dependencies


_local_funcs = FunctionToolset[Dependencies]()


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


# If you make other toolsets, add them here.
# This is what is loaded into the bot.
main_toolset = CombinedToolset[Dependencies]([_local_funcs]).filtered(
    lambda ctx, tool: ctx.deps.env.environment == "dev" or not tool.name.startswith("dev_")
)
