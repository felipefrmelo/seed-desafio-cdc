from abc import ABC, abstractmethod
from typing import List, Optional, TypedDict
from typing_extensions import NotRequired


class ErrorDescription(TypedDict):
    message: str
    field: NotRequired[Optional[str]]


class BaseHTTPException(Exception, ABC):
    status_code = 400

    @abstractmethod
    def serialize(self) -> List[ErrorDescription]:
        pass
