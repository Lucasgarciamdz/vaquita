# base_repo.py
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session
from config.logger_config import setup_custom_logger
import hashlib

class BaseRepo:
    logged_operations = set()  # Make logged_operations a class variable

    def __init__(self, model, session: scoped_session):
        self.model = model
        self.session = session
        self.log = setup_custom_logger(self.__class__.__name__)

    def add(self, entity):
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        self._log_info_once("add", entity=entity)

    def get(self, id):
        entity = self.session.query(self.model).get(id)
        self._log_info_once("get", id=id, entity=entity)
        return entity

    def get_all(self):
        entities = self.session.query(self.model).all()
        self._log_info_once("get_all", entities=entities)
        return entities

    def update(self, entity):
        try:
            self.session.merge(entity)
            self.session.commit()
            self._log_info_once("update", entity=entity)
        except SQLAlchemyError:
            self.session.rollback()
            self.log.exception("Failed to update entity")

    def delete(self, entity):
        try:
            self.session.delete(entity)
            self.session.commit()
            self._log_info_once("delete", entity=entity)
        except SQLAlchemyError:
            self.session.rollback()
            self.log.exception("Failed to delete entity")

    def _log_info_once(self, operation, **kwargs):
        key = self._generate_operation_key(operation, **kwargs)
        if key not in self.logged_operations:
            message = f"{operation.capitalize()} operation: {kwargs}"
            print(message)
            self.logged_operations.add(key)

    def _generate_operation_key(self, operation, **kwargs):
        # If 'entity' is in kwargs and it has an 'id' attribute, use only the operation and entity ID for the key
        entity = kwargs.get('entity')
        if entity and hasattr(entity, 'id'):
            key_str = f"{operation}:{entity.id}"
        else:
            # Fallback to using all kwargs if 'entity' or 'entity.id' is not available
            sorted_kwargs = sorted(kwargs.items())
            key_str = f"{operation}:{sorted_kwargs}"
        return hashlib.md5(key_str.encode()).hexdigest()