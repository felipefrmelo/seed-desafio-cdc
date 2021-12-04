from logging import debug
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session

from casadocodigo.ensure import ensure_this_field_has_no_duplicate
from casadocodigo.service_layer.In import CountryCreate, StateCreate
from casadocodigo.service_layer.Out import CountryOut, StateOut
from casadocodigo.service_layer.errors import CountryNotFound

from ..dependencies import get_db
from ..domain.models import Country, State


app = APIRouter(prefix="/country", tags=["country"])


@app.post("/", response_model=CountryOut, status_code=201)
def create_country(country: CountryCreate, db: Session = Depends(get_db)):
    ensure_this_field_has_no_duplicate(
        db, Country, name=country.name)

    db_country = country.to_model()
    db.add(db_country)
    db.commit()
    return db_country


@app.post("/{country_id}/state", response_model=StateOut, status_code=201)
def create_state(
        country_id: int, state: StateCreate, db: Session = Depends(get_db)):
    country = db.query(Country).get(country_id)

    if not country:
        raise CountryNotFound()

    ensure_this_field_has_no_duplicate(
        db, State, name=state.name)

    country.create_state(state.to_model())
    db.commit()
    return state
