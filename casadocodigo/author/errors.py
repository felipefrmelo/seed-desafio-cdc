from typing import List
from casadocodigo.errors import BaseHTTPException, ErrorDescription



class EmailAlredyExist(BaseHTTPException):
    status_code = 400

    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def serialize(self) -> List[ErrorDescription]:
        return [{"message": "email already exists", 'field': "email"}]
