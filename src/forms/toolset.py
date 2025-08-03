from typing import Literal
from pydantic_ai import RunContext
from pydantic_ai.toolsets import FunctionToolset

from chat.types import Dependencies
from forms.test_form import IthakaEvaluationSupportForm
from forms.types import BadInput


form_tools = FunctionToolset[Dependencies]()


@form_tools.tool
def complete_form(
    _ctx: RunContext[Dependencies], form: IthakaEvaluationSupportForm
) -> Literal["Success", "Failure"] | BadInput:
    """
    Complete a form based on the information provided by the user. If the user
    presents the intention of completing the form, but does not provide enough
    information, ask them for the missing information, be as helpful as possible.

    Once all the information is provided, call this tool and notify the user
    of the state.

    If you have some information, but there are unspecified fields, ask the
    user if they would like to complete the other fields, even if they are
    optional. Do not just list them; briefly describe what they would contain
    naturally.

    Args:
        :form: The form to fill.

    Returns:
        Whether the transaction was succesful, a failure, or the input provided
        was bad.
    """

    # TODO: Implement
    print(f"{form = }")

    return "Success"
