from pydantic.main import BaseModel

from . import model


class CategoryCreate(BaseModel):
    name: str

    def to_model(self):
        return model.Category(self.name)


class CategoryOut(BaseModel):
    id: int
    name: str
