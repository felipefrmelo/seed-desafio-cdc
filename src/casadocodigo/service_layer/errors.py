
from abc import abstractmethod
from typing import List, Optional, TypedDict
from typing_extensions import NotRequired


class ErrorDescription(TypedDict):
    message: str
    field: NotRequired[Optional[str]]


class BaseException(Exception):

    @abstractmethod
    def serialize(exception) -> List[ErrorDescription]:
        pass


class NotFound(BaseException):
    entity = 'entity'

    def serialize(self) -> List[ErrorDescription]:
        return [{'message': f'{self.entity} not found'}]


class AuthorNotFound(NotFound):
    entity = 'author'


class CategoryNotFound(NotFound):
    entity = 'category'


class BookNotFound(NotFound):
    entity = 'book'
