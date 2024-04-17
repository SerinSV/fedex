import time
from typing import Any, List, Optional

from pydantic import BaseModel

from scripts.constants import STATUS


def get_current_time():
    return int(time.time() * 1000)


class DefaultResponse(BaseModel):
    status: str = STATUS.SUCCESS
    message: Optional[str]
    data: Optional[Any]
    # svts: int = Field(default_factory=get_current_time)


class DefaultFailureResponse(DefaultResponse):
    status: str = STATUS.FAILED
    error: Any


class TableResponse(BaseModel):
    headerContent: List
    bodyContent: List
