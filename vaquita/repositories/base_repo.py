from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class BaseRepo:
    def __init__(self, model, session: Session):
        self.model = model
        self.session = session

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()

    def get(self, id):
        return self.session.query(self.model).get(id)

    def get_all(self):
        return self.session.query(self.model).all()

    def update(self, entity):
        try:
            self.session.merge(entity)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()

    def delete(self, entity):
        try:
            self.session.delete(entity)
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()