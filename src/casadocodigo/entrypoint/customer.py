from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm.session import Session
from casadocodigo.domain.models import Country, Customer
from casadocodigo.ensure import ensure_this_field_has_no_duplicate

from casadocodigo.service_layer.In import  CustomerCreate, PaymentCreate
from casadocodigo.service_layer.Out import CustomerOut, PaymentOut, PaymentOutDetail
from casadocodigo.service_layer.errors import CountryNotFound, ValidationException

from ..dependencies import get_db


app = APIRouter(prefix="/customer", tags=["customer"])





@app.post("/", response_model=CustomerOut,  status_code=201)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    ensure_this_field_has_no_duplicate(
        db, Customer, email=customer.email)
        
    country: Country = db.query(Country).filter_by(
        id=customer.country_id).first()

    if not country:
        raise CountryNotFound()

    if customer.state_name:
        state = country.get_state(customer.state_name)
        if not state:
            raise ValidationException("state must be belong to country")

    customer_db = customer.to_model(country)
    db.add(customer_db)
    db.commit()
    return customer_db