from datetime import datetime, timezone

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from pydantic.fields import Field

app = FastAPI()


class BaseUser(BaseModel):
    name: str
    description: str = Field(
        title="The description of the item", max_length=400)
    email: EmailStr


class UserCreate(BaseUser):
    pass


class User(BaseUser):
    createdAt: datetime


@app.post("/author/", response_model=User, status_code=201)
def create_user(user: UserCreate):

    createdAt = datetime.now(timezone.utc)
    return User(**user.dict(), createdAt=createdAt)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"message": e['msg'], 'field': e['loc'][1]}for e in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": errors}
    )
