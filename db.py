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

    def __init__(self, db_file=None):

        # If DB connection initialized already
        if db_file is not None or self.engine is None:

            # If no DB file passed, use default
            db_file = db_file or DB_FILE

            # Connect to the DB
            self.switch_database(db_file)

    @staticmethod
    def connect(db_file):
        """ Creates connection. """

        # If engine isn't initialized yet
        if DB.engine is None:

            # Initialize an engine
            DB.engine = create_engine(SQLITE_URI_PREF+db_file)

            # Initialize sessions
            session = sessionmaker()
            session.configure(bind=DB.engine)
            DB.session = session()

    def switch_database(self, db_file):
        """ Switch to a new database file. """

        # If connection is initialized already
        if DB.engine is not None and DB.session is not None:
            # If the file is different from the one stored in the Class
            if DB.db_file != db_file:
                # Reinitialized the connection
                self.disconnect()
                self.connect(db_file)

        # If the connection isn't initialized
        else:
            # Initialize the connection
            self.connect(db_file)

        # (Re)set the DB file location
        DB.db_file = db_file

    @staticmethod
    def disconnect():
        """ Close the connection and all the sessions. """
        # Close the connection if it is opened
        if DB.engine is not None:
            DB.engine.dispose()
            DB.engine = None
        # Close the session if it is opened
        if DB.session is not None:
            DB.session.close()
            DB.session = None

    def tearDown(self):
        self.disconnect()
