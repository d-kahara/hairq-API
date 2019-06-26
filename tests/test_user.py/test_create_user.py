from tests.base import BaseTestCase
from fixtures.user.user_fixture import (
    user_mutation_query, user_mutation_response
)

from helpers.database import db_session


class TestCreateUser(BaseTestCase):
    def test_user_creation(self):
        """
        Tests User creation
        """
        query = self.client.execute(
            user_mutation_query,
            context={'session': db_session}
        )
        self.assertEqual(query, user_mutation_response)
