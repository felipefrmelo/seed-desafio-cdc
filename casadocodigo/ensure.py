from typing import List
from casadocodigo.errors import BaseHTTPException, ErrorDescription


class ValueAlredyExist(BaseHTTPException):
    status_code = 400

    def __init__(self, field_name) -> None:
        self.field_name = field_name

    def serialize(self) -> List[ErrorDescription]:
        return [{"message": f"{self.field_name} already exists", 'field': self.field_name}]


def ensure_this_field_has_no_duplicate(get_field, field_name, *args):
    if get_field(*args):
        raise ValueAlredyExist(field_name)
