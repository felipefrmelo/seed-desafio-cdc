
from fastapi import Depends, APIRouter
from sqlalchemy.orm.session import Session

from casadocodigo.ensure import ensure_this_field_has_no_duplicate
from . import dtos, model
from ..dependencies import get_db

app = APIRouter(prefix="/category", tags=["category"])


@app.post("/", response_model=dtos.CategoryOut, status_code=201)
def create_category(category: dtos.CategoryCreate, db: Session = Depends(get_db)):

    ensure_this_field_has_no_duplicate(
        db, model.Category, "name", category.name)

    db_category = category.to_model()
    db.add(db_category)
    db.commit()
    return db_category
