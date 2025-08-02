from random import random
from typing import Literal
from pydantic import BaseModel
from chat.tool_use.decorator import ToolBag, tool
from env import env


# Always use pydantic models for complex objects.
class ExampleParam(BaseModel):
    myParam: str
    """
    Dumy value. Set it to "wassup".
    """

    someEnum: Literal["howdy", "dowdy!", "so based!"]
    """
    Choose one of these randomly.
    """

class ExampleBag(ToolBag):
    @tool(env().environment == "dev")
    @staticmethod
    def example_tool_func(param: ExampleParam) -> float:
        """
        This is an example function call to show developers.
        Show it when asked for the test function.

        Parameters:
            :param: Example param value.

        Returns:
            A random number.
        """
        output = random()

        print(f"Hi from example tool. {output = }")
        print(f"{param = }")

        return output
