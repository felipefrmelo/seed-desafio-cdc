

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from casadocodigo.errors import BaseHTTPException
from casadocodigo.service_layer.errors import NotFound, BaseException
from .orm import metadata
from .database import engine
from .entrypoint.category import app as CategoryRouter
from .entrypoint.author import app as EntrypointAuthorRouter
from .entrypoint.books import app as EntrypointBookRouter
from .entrypoint.countries import app as EntrypointCountryRouter
from .entrypoint.payment import app as EntrypointPaymentRouter
from .entrypoint.cupom import app as EntrypointCupomRouter

app = FastAPI()

metadata.create_all(engine)


app.include_router(EntrypointAuthorRouter)
app.include_router(CategoryRouter)
app.include_router(EntrypointBookRouter)
app.include_router(EntrypointCountryRouter)
app.include_router(EntrypointPaymentRouter)
app.include_router(EntrypointCupomRouter)


@app.exception_handler(NotFound)
async def handle_unprocessable_entity(request: Request, exc: NotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"errors": exc.serialize()},
    )


@app.exception_handler(BaseException)
async def handle_unprocessable_entity(request: Request, exc: BaseException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"errors": exc.serialize()},
    )


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
