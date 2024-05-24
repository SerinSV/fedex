import time
from typing import Any, Optional

from pydantic import BaseModel

from scripts.constants import STATUS


class DefaultResponse(BaseModel):
    status: str = STATUS.SUCCESS
    message: Optional[str]
    data: Optional[Any]
    # svts: int = Field(default_factory=get_current_time)


class DefaultFailureResponse(DefaultResponse):
    status: str = STATUS.FAILED
    error: Any
