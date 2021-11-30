
from datetime import datetime
from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr

from . import model


class BaseAuthor(BaseModel):
    name: str
    description: str = Field(
        title="The description of the item", max_length=400)
    email: EmailStr


class AuthorCreate(BaseAuthor):

    def to_model(self):
        return model.Author(name=self.name, description=self.description, email=self.email)


class AuthorOut(BaseAuthor):
    id: int
    books: list
    created_at: datetime
