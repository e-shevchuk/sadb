import unittest

from .data_model import VerySimpleDBObject, apply_model
from .db import DB
from .service import use_test_db


# CONSTANTS

# Names for testing
ROBIN = 'Robin'
BATMAN = 'Batman'


# TEST CASES

class DBTests(unittest.TestCase):

    def setUp(self):
        DB.apply_model_func = apply_model

    def tearDown(self):
        DB.disconnect(remove_db_file=True)

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
            b = fdb.session.query(VerySimpleDBObject) \
                .filter_by(**flt).one_or_none()

            return b

        # Switch to the test DB
        db = DB(recreate=True)
        # Create a test object
        create_test_obj(BATMAN)
        # Check that it is visible
        self.assertIsNotNone(select_user(db, BATMAN))

        # Create a user in wrapped call, and make sure that it is created
        # inside the wrapper. Then leave the wrapper, after which the DB
        # in which it was created should be dropped => it will not be here
        create_test_obj_wrapped(ROBIN)
        # Check that user isn't available
        self.assertIsNone(select_user(db, ROBIN))

    @use_test_db
    def test_03_apply_model_to_an_existing_db(self):
        """ Tests applying the model to an initialized DB. """

        # Apply the model to the DB
        db = DB(apply_model_func=apply_model)

        # Create the test object
        db.session.add(VerySimpleDBObject(name='Varis'))
        # Add the test object to the DB
        db.session.commit()
        db.session.query(VerySimpleDBObject).all()

        # Check that the object is created
        self.assertEqual(db.session.query(VerySimpleDBObject)[0].name, 'Varis')
