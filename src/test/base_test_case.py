import os
import tempfile
import unittest

from controller.app import app
from infrastructure.database import (
    db_connect,
    init_db_engine
)


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        db_engine = self._build_test_db()
        self.app = app
        self.app.config.update(
            TESTING=True,
            DEBUG=True,
            WTF_CSRF_ENABLED=False,
            DB_ENGINE=db_engine
        )
        self.client = self.app.test_client()
        self.db_connection = db_connect(db_engine)

    def tearDown(self):
        os.close(self.db_file_descriptor)
        os.unlink(self.db_file_path)

    def _build_test_db(self):
        self.db_file_descriptor, self.db_file_path = tempfile.mkstemp()
        return init_db_engine(db_uri=f"sqlite:///{self.db_file_path}")
