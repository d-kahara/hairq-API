import enum
from helpers.database import db_session


<<<<<<< HEAD
class Utility(object):
=======
class ModelOperations(object):
>>>>>>> 2274939ae6978efa5dbb73c0d35d66e41bfb60d9
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
