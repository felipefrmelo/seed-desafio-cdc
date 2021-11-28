
from fastapi import Depends, APIRouter
from sqlalchemy.orm.session import Session
from . import dtos, model
from .errors import EmailAlredyExist
from ..dependencies import get_db

app = APIRouter(prefix="/author", tags=["author"])


def get_user_by_email(db: Session, email: str):
    return db.query(model.Author).filter_by(email=email).first()


@app.post("/", response_model=dtos.AuthorOut, status_code=201)
def create_user(user: dtos.AuthorCreate, db: Session = Depends(get_db)):
    user_exist = get_user_by_email(db, user.email)
    if user_exist:
        raise EmailAlredyExist()

    db_user = user.to_model()
    db.add(db_user)
    db.commit()
    return db_user
