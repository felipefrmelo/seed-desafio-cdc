from typing import List

from sqlalchemy.orm.session import Session
from casadocodigo.errors import BaseHTTPException, ErrorDescription


class ValueAlredyExist(BaseHTTPException):
    status_code = 400

    def __init__(self, field_name) -> None:
        self.field_name = field_name

    def serialize(self) -> List[ErrorDescription]:
        return [{"message": f"{self.field_name} already exists", 'field': self.field_name}]


def ensure_this_field_has_no_duplicate(db: Session, model, field, value):
    if db.query(model).filter_by(**{field: value}).first():
        raise ValueAlredyExist(field)
