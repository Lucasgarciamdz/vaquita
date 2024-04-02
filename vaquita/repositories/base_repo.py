from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from vaquita.config.logger_config import setup_custom_logger


class BaseRepo:
    def __init__(self, model, session: Session):
        self.model = model
        self.session = session
        self.log = setup_custom_logger(self.__class__.__name__)

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()
        self.log.info(f"Added entity: {entity}")

    def get(self, id):
        entity = self.session.query(self.model).get(id)
        self.log.info(f"Got entity with id {id}: {entity}")
        return entity

    def get_all(self):
        entities = self.session.query(self.model).all()
        self.log.info(f"Got all entities: {entities}")
        return entities

    def update(self, entity):
        try:
            self.session.merge(entity)
            self.session.commit()
            self.log.info(f"Updated entity: {entity}")
        except SQLAlchemyError:
            self.session.rollback()
            self.log.exception("Failed to update entity")

    def delete(self, entity):
        try:
            self.session.delete(entity)
            self.session.commit()
            self.log.info(f"Deleted entity: {entity}")
        except SQLAlchemyError:
            self.session.rollback()
            self.log.exception("Failed to delete entity")
