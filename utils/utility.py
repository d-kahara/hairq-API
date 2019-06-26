import enum
from helpers.database import db_session


class Utility(object):
    def save(self):
        """Function that saves new objects"""
        db_session.add(self)
        db_session.commit()

    def delete(self):
        """Function that deletes objects"""
        db_session.delete(self)
        db_session.commit()


class StateType(enum.Enum):
    active = 'active'
    archived = 'archived'
    deleted = 'deleted'
