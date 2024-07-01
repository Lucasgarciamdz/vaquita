# base_repo.py
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session
from config.logger_config import setup_custom_logger


class BaseRepo:
    def __init__(self, model, session: scoped_session):
        self.model = model
        self.session = session
        self.log = setup_custom_logger(self.__class__.__name__)
        self.logged_messages = set()

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        self._log_info_once(f"Added entity: {entity}")

    def get(self, id):
        entity = self.session.query(self.model).get(id)
        self._log_info_once(f"Got entity with id {id}: {entity}")
        return entity

    def get_all(self):
        entities = self.session.query(self.model).all()
        self._log_info_once(f"Got all entities: {entities}")
        return entities

    def update(self, entity):
        try:
            self.session.merge(entity)
            self.session.commit()
            self._log_info_once(f"Updated entity: {entity}")
        except SQLAlchemyError:
            self.session.rollback()
            self.log.exception("Failed to update entity")

    def delete(self, entity):
        try:
            self.session.delete(entity)
            self.session.commit()
            self._log_info_once(f"Deleted entity: {entity}")
        except SQLAlchemyError:
            self.session.rollback()
            self.log.exception("Failed to delete entity")

    def _log_info_once(self, message):
        if message not in self.logged_messages:
            self.log.info(message)
            self.logged_messages.add(message)
