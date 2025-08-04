from typing import Literal
from uuid import UUID
from pydantic import BaseModel


class BadInput(BaseModel):
    """
    Information about why the input processing failed.
    """
    discriminator: Literal["Bad input"] = "Bad input"
    bad_input_explanation: str

class FormInformation(BaseModel):
    discriminator: Literal["Success"] = "Success"
    form_id: UUID

class ErrorResult(BaseModel):
    discriminator: Literal["Failure"] = "Failure"
    error_explanation: str
