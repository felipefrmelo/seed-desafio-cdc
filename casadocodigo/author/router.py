
from fastapi import Depends, APIRouter
from sqlalchemy.orm.session import Session

from casadocodigo.ensure import ensure_this_field_has_no_duplicate
from . import dtos, model
from ..dependencies import get_db

app = APIRouter(prefix="/author", tags=["author"])


def get_user_by_email(db: Session, email: str):
    return db.query(model.Author).filter_by(email=email).first()


@app.post("/", response_model=dtos.AuthorOut, status_code=201)
def create_user(user: dtos.AuthorCreate, db: Session = Depends(get_db)):
    ensure_this_field_has_no_duplicate(
        get_user_by_email, "email", db, user.email)

    db_user = user.to_model()
    db.add(db_user)
    db.commit()
    return db_user
