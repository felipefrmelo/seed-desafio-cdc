from fastapi import Depends, APIRouter
from sqlalchemy.orm.session import Session

from casadocodigo.ensure import ensure_this_field_has_no_duplicate
from ..dependencies import get_db
from ..domain.models import Cupom
from casadocodigo.service_layer.In import CupomCreate
from casadocodigo.service_layer.Out import CupomOut


app = APIRouter(prefix="/cupoms", tags=["cupom"])


@app.post("/", response_model=CupomOut, status_code=201)
def create_cupom(cupom: CupomCreate, db: Session = Depends(get_db)):
    ensure_this_field_has_no_duplicate(
        db, Cupom, code=cupom.code)

    cupom_db = cupom.to_model()
    db.add(cupom_db)
    db.commit()

    return cupom_db
