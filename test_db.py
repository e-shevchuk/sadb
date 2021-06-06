import unittest

from .data_model import VerySimpleDBObject
from .db import DB
from .service import use_test_db, recreate_sqlite_db, get_temporary_db_file


# TEST CASES

class DBTests(unittest.TestCase):

    def test_01_init(self):
        """Testing DB connection initialization"""

        # Get the budget
        db = DB()

        self.assertTrue(db.session)

    def test_02_service_use_test_db(self):
        """Testing service function use temporary DB function. """

        def create_test_obj(name='Batman'):
            tobj = VerySimpleDBObject(name=name)
            db.session.add(tobj)
            db.session.commit()

        @use_test_db
        def create_test_obj_wrapped(name):
            create_test_obj(name)
            # Check that user isn't available
            fdb = DB()
            self.assertIsNotNone(select_user(fdb, name))

        def select_user(fdb, name='Batman'):
            flt = {"name": name}
            b = fdb.session.query(VerySimpleDBObject).filter_by(**flt).one_or_none()
            return b

        # TMP DB File
        tmp_db_file = get_temporary_db_file()
        # Refresh the test DB
        recreate_sqlite_db(tmp_db_file)
        # Switch to the test DB
        db = DB(tmp_db_file)
        # Create a test object
        create_test_obj()
        # Check that it is visible
        self.assertIsNotNone(select_user(db))

        # Create a user in wrapped call, where
        # the test DB should have been dropped
        name2 = 'Robin'
        create_test_obj_wrapped(name2)
        # Check that user isn't available
        # TODO: Passes with any str value at the name2 place, while should not
        self.assertIsNone(select_user(db, name2))
