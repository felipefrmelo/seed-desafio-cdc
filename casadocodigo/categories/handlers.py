from sqlalchemy.orm.session import Session

from casadocodigo.categories.model import Category


def get_category(session: Session, category_id: int) -> Category:
    return session.query(Category).get(category_id)
