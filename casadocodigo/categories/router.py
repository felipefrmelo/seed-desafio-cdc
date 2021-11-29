
from fastapi import Depends, APIRouter
from sqlalchemy.orm.session import Session

from casadocodigo.ensure import ensure_this_field_has_no_duplicate
from . import dtos, model
from ..dependencies import get_db

app = APIRouter(prefix="/category", tags=["category"])


def get_category_by_name(db: Session, name: str):
    return db.query(model.Category).filter_by(name=name).first()


@app.post("/", response_model=dtos.CategoryOut, status_code=201)
def create_category(category: dtos.CategoryCreate, db: Session = Depends(get_db)):
    ensure_this_field_has_no_duplicate(
        get_category_by_name, "category", db, category.name)

    db_category = category.to_model()
    db.add(db_category)
    db.commit()
    return db_category
