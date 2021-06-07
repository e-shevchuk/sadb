import os
import unittest
from datetime import datetime

from .service import get_temp_dir
from .db import DB
from .data_model import apply_model


# TEST CASES

class ServiceTests(unittest.TestCase):

    def setUp(self):
        DB.apply_model_func = apply_model

    def tearDown(self):
        DB.disconnect(remove_db_file=True)

    def test_01_get_temp_dir(self):
        """ Tests temporary directory creating. """

        # Shape-up some pseudo-random directory name
        test_dir_name = f"tmp_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        # Create and the the temp dir path
        p, just_created = get_temp_dir(test_dir_name)
        # Check that it exists
        self.assertTrue(os.path.isdir(p))
        # If it was just created
        if just_created:
            # Remove the temporary directory
            os.rmdir(p)
