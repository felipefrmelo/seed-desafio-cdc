from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, TypedDict
from typing_extensions import NotRequired

from fastapi import Depends, FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from pydantic.fields import Field
from sqlalchemy.orm.session import Session
from .orm import engine, SessionLocal, metadata
from . import model
from . import dtos
from .errors import EmailAlredyExist, BaseHTTPException

app = FastAPI()

metadata.create_all(engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()  # type: ignore


def get_user_by_email(db: Session, email: str):
    return db.query(model.Author).filter_by(email=email).first()


@app.post("/author/", response_model=dtos.AuthorOut, status_code=201)
def create_user(user: dtos.AuthorCreate, db: Session = Depends(get_db)):
    user_exist = get_user_by_email(db, user.email)
    if user_exist:
        raise EmailAlredyExist()

    db_user = user.to_model()
    db.add(db_user)
    db.commit()
    return db_user


@app.exception_handler(BaseHTTPException)
async def exception_handler(request: Request, exc: BaseHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"errors": exc.serialize()}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"message": e['msg'], 'field': e['loc'][1]}for e in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"errors": errors}
    )
