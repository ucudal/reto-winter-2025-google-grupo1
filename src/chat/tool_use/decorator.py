from typing import Callable


def tool[Params, Return](
    enabled: bool = True,
) -> Callable[[Callable[[Params], Return]], Callable[[Params], Return]]:
    """
    A decorator to conditionally register a function as a global tool at declaration time.

    If `enabled` is True, the function is added to the global toolset.
    The original function is always returned, allowing it to be called normally.

    Args:
        enabled: A boolean flag to enable or disable tool registration.

    Returns:
        The decorator that wraps the function.
    """

    def decorator(func: Callable[[Params], Return]) -> staticmethod[[Params], Return]:
        func.__is_tool = enabled # pyright: ignore[reportFunctionMemberAccess]
        return staticmethod(func)

    return decorator

class ToolBag:
    @classmethod
    def get_tools(cls) -> frozenset[Callable[..., object]]:
        tools = {
            attr.__func__
            for attr in cls.__dict__.values() # pyright: ignore[reportAny]
            if isinstance(attr, staticmethod) and getattr(attr.__func__, '__is_tool', False)
        }
        return frozenset(tools)
