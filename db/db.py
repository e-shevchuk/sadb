import errno
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


# CONSTANTS

DB_FILE = 'data.db'
SQLITE_URI_PREF = "sqlite:///"


# DB CONNECTOR CLASS

class DB:

    engine = None
    session = None
    db_file = None
    apply_model_func = None

    def __init__(self, db_file=None, recreate=False, apply_model_func=None):

        # Save the model Base class, if passed
        DB.apply_model_func = apply_model_func or DB.apply_model_func

        # If DB connection initialized already
        if db_file is not None or self.engine is None or apply_model_func:

            # If no DB file passed, use default
            db_file = db_file or DB_FILE

            # Connect to the DB
            self.switch_database(db_file, recreate, apply_model_func)

    def initialize_db(self, db_file=None):
        """ Initialize the Database connection. """

        # If no DB file passed, use default
        db_file = db_file or DB_FILE

        # Connect to the DB
        self.switch_database(db_file)

    @staticmethod
    def connect(db_file):
        """ Creates connection. """

        # If engine isn't initialized
        if DB.engine is None and DB.session is None:

            # Initialize an engine
            DB.engine = create_engine(SQLITE_URI_PREF+db_file)
            DB.db_file = db_file

            # Initialize sessions
            session = sessionmaker()
            session.configure(bind=DB.engine)
            DB.session = session()

    def switch_database(self, db_file, recreate=False, apply_model_func=None):
        """ Switch to a new database file. """

        # If connection is initialized already
        if DB.engine is not None and DB.session is not None:
            # If the file is different from the one stored in the Class
            if DB.db_file != db_file or recreate:
                # Disconnect from the DB
                self.disconnect(remove_db_file=recreate)
                # Connect to the new DB file
                self.connect(db_file)

        # If the connection isn't initialized
        else:
            # If DB should be re-created, remove the new db_file first
            DB.db_file = db_file
            recreate and self.remove_db_file()
            # Initialize the connection
            self.connect(db_file)

        # (Re)set the DB file location
        DB.db_file = db_file

        # If ORM model base class is provided
        if apply_model_func is not None or DB.apply_model_func is not None:
            # Apply the ORM Model
            self.apply_model(apply_model_func)

    def apply_model(self, apply_model_func):
        """ Applies the ORM to the database. """

        # Save the DB model if it was passed
        DB.apply_model_func = apply_model_func or DB.apply_model_func

        # If the model Base wasn't provided - throw an error
        err_msg = 'Can\'t apply model without the model Base class'
        assert DB.apply_model_func is not None, err_msg

        # If the engine is not initialized - throw an error
        err_msg = 'Applying model needs an initialized DB connection. '
        assert DB.engine is not None and DB.session is not None, err_msg

        # Apply the model
        DB.apply_model_func(self.engine)

    @staticmethod
    def disconnect(remove_db_file=False):
        """ Close the connection and all the sessions. """

        # Close the connection if it is opened
        if DB.engine is not None:
            DB.engine.dispose()
            DB.engine = None
        # Close the session if it is opened
        if DB.session is not None:
            DB.session.close()
            DB.session = None
        # Remove the DB file if it is requested
        if remove_db_file:
            DB.remove_db_file()

    @staticmethod
    def remove_db_file():
        """ Removes the file, if it doesn't exist, do nothing. """

        # If DB connection isn't terminated yet - throw an error
        err_msg = 'Can\'t remove the DB file while connection is active.'
        assert DB.engine is None and DB.session is None, err_msg

        try:
            # Try to remove the file
            os.remove(DB.db_file)

        # If failed to remove
        except OSError as e:
            # If the reason is different then the file non-existence
            if e.errno != errno.ENOENT:
                # Re-rise the exception
                raise

    def tearDown(self):
        self.disconnect()
