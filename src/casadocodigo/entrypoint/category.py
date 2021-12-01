from fastapi import Depends, APIRouter
from sqlalchemy.orm.session import Session

from casadocodigo.ensure import ensure_this_field_has_no_duplicate
from ..dependencies import get_db
from ..domain.models import Category
from casadocodigo.service_layer.In import CategoryCreate
from casadocodigo.service_layer.Out import CategoryOut
app = APIRouter(prefix="/category", tags=["category"])




@app.post("/", response_model=CategoryOut, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):

    ensure_this_field_has_no_duplicate(
        db, Category, "name", category.name)

    db_category = category.to_model()
    db.add(db_category)
    db.commit()
    return db_category
