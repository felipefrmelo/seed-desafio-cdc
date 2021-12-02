from typing import List

from sqlalchemy.orm.session import Session
from casadocodigo.errors import BaseHTTPException, ErrorDescription


class ValueAlredyExist(BaseHTTPException):
    status_code = 400

    def __init__(self, fields: dict) -> None:
        self.fields = fields

    def serialize(self) -> List[ErrorDescription]:
        return [{'message': f"{field} already exists", 'field': field} for field in self.fields]


def ensure_this_field_has_no_duplicate(db: Session, model, **fields):
    fields_alredy_exist = get_fields_that_already_exist(fields, db, model)
    if fields_alredy_exist:
        raise ValueAlredyExist(fields_alredy_exist)


def get_fields_that_already_exist(fields, db, model):
    return {field: value for field, value in fields.items()
            if db.query(model).filter_by(**{field: value}).first()}
