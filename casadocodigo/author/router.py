
from fastapi import Depends, APIRouter
from sqlalchemy.orm.session import Session

from casadocodigo.ensure import ensure_this_field_has_no_duplicate
from . import dtos, model
from ..dependencies import get_db

app = APIRouter(prefix="/author", tags=["author"])


@app.post("/", response_model=dtos.AuthorOut, status_code=201)
def create_user(user: dtos.AuthorCreate, db: Session = Depends(get_db)):

    ensure_this_field_has_no_duplicate(
        db, model.Author, "email", user.email)

    db_user = user.to_model()
    db.add(db_user)
    db.commit()
    return db_user
