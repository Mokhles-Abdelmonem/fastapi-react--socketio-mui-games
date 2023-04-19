from pydantic import BaseModel, Field
from typing import Union


class MessageJson(BaseModel):
    """
    """
    text: Union[str, None] = None

class BaseRuleJson(BaseModel):
    """
    """
    winning_number: int = Field(ge=1)

class RuleJson(BaseRuleJson):
    """
    """
    timer: Union[int, None] = None
    rules: list[list[int]]


class BoardJson(BaseModel):
    """
    """
    board: list[list[str]] 