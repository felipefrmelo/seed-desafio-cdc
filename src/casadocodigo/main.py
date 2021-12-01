

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from casadocodigo.errors import BaseHTTPException
from .orm import metadata
from .database import engine
from .entrypoint.category import app as CategoryRouter
from .entrypoint.author import app as EntrypointAuthorRouter
app = FastAPI()

metadata.create_all(engine)


app.include_router(EntrypointAuthorRouter)
app.include_router(CategoryRouter)


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
