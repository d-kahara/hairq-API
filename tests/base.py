from flask_testing import TestCase
from graphene.test import Client
from alembic import command, config

from app import create_app
from schema import schema
from helpers.database import Base, db_session, engine


class BaseTestCase(TestCase):
    alembic_configuration = config.Config("./alembic.ini")

    def create_app(self):
        app = create_app("testing")
        self.client = Client(schema)
        return app

    def setUp(self):
        app = self.create_app()
        self.app_test = app.test_client()
        with app.app_context():
            Base.metadata.create_all(bind=engine)

            command.stamp(self.alembic_configuration, 'head')
            command.downgrade(self.alembic_configuration, '-1')
            command.upgrade(self.alembic_configuration, 'head')
            db_session.commit()

    def tearDown(self):
        app = self.create_app()
        with app.app_context():
            command.stamp(self.alembic_configuration, "base")
            db_session.remove()
            Base.metadata.drop_all(bind=engine)
