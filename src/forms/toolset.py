from uuid import UUID, uuid4
from pydantic_ai import RunContext
from pydantic_ai.toolsets import FunctionToolset

from chat.types import Dependencies
from forms.test_form import IthakaEvaluationSupportForm
from forms.types import BadInput, ErrorResult, FormInformation


form_tools = FunctionToolset[Dependencies]()

# Pretend this is storage for now
_forms = dict[UUID, IthakaEvaluationSupportForm]()


@form_tools.tool
def complete_form(
    _ctx: RunContext[Dependencies], form: IthakaEvaluationSupportForm, form_id: UUID | None = None
) -> FormInformation | BadInput | ErrorResult:
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

    Before calling this tool, ask the user if they want to commit that
    information; list what you have understood.

    Args:
        :form: The data to fill the form with.
        :form_id: If set, the given data will overwrite the form with that id.

    Returns:
        Whether the transaction was succesful, a failure, or the input provided
        was bad.
    """
    print(f"Completing {form_id = }")
    if form_id is not None and _forms.get(form_id) is None:
        return BadInput(bad_input_explanation="Form with that id does not exist")

    if form_id is None:
        form_id = uuid4()

    print(f"{form = }")
    _forms[form_id] = form

    return FormInformation(form_id=form_id)


@form_tools.tool
def get_form(_ctx: RunContext[Dependencies], form_id: UUID) -> IthakaEvaluationSupportForm | BadInput | ErrorResult:
    """
    Get the form with id :form_id:.

    Args:
        :form_id: The id with which to retrieve the form.

    Returns:
        The form, error, or if the input was incorrect.

    """
    print(f"Getting {form_id = }")
    form = _forms.get(form_id)

    if form is None:
        return BadInput(bad_input_explanation="Form with that id does not exist.")

    print(f"{form = }")
    return form
