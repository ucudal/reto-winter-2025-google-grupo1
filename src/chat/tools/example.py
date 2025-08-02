from random import random
from typing import Literal
from pydantic import BaseModel, Field


# Always use pydantic models for complex objects.
class ExampleParam(BaseModel):
    myParam: str
    someEnum: Literal["howdy", "dowdy!", "so based!"]

def example_tool_func(param: ExampleParam) -> float:
    """
    This is an example function call to show developers.
    Show it when asked for the test function.

    You should make up the parameter values. If you are told to generate
    incorrect values, try to do so and report the result.

    Parameters:
        :param: Example param value.

    Returns:
        A random number.
    """
    output = random()

    print(f"Hi from example tool. {output = }")
    print(f"{param = }")

    return output
