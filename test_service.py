import os
from datetime import datetime
import unittest
from .service import get_temp_dir


# TEST CASES

class ServiceTests(unittest.TestCase):

    def test_01_get_temp_dir(self):
        """ Tests temporary directory creating. """

        # Shape-up some pseudo-random directory name
        test_dir_name = f"tmp_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        # Create and the the temp dir path
        p = get_temp_dir(test_dir_name)
        # Check that it exists
        self.assertTrue(os.path.isdir(p))
        # Remove the temporary directory
        os.rmdir(p)
