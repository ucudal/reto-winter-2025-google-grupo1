from typing import Callable

# Lsp complains cause the type is a variable, technically.
def call_func(func: Callable[..., object], params: dict[str, object]) -> object:
    return func(**params)
