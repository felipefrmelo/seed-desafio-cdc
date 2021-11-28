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
        """docstring for serialize"""


class EmailAlredyExist(BaseHTTPException):
    status_code = 400

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def serialize(self) -> List[ErrorDescription]:
        return [{"message": "email already exists", 'field': "email"}]
