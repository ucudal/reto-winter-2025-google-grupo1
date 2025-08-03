from uuid import UUID
from pydantic import BaseModel


class BadInput(BaseModel):
    """
    Information about why the input processing failed.
    """
    bad_input_explanation: str

class FormInformation(BaseModel):
    form_id: UUID
