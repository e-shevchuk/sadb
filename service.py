import os
from datetime import datetime

from db import DB, DB_FILE


# CONSTANTS

TEMP = 'temp/'


# FUNCTIONS

def get_temp_dir(temp_dir_name=TEMP):
    """ Returns the full path to the temporary directory. """

    # Shape up the full directory path
    path = os.path.abspath(temp_dir_name) + '/'
    # If the temporary directory exists
    if os.path.isdir(path):
        # Return the directory
        return path
    # If the directory doesn't exist
    else:
        # Create it
        os.makedirs(path, exist_ok=True)
        # Return the created directory path
        return path


def file_name_temporize(file_name):
    """Return the file name with timestamp appended right before extension"""

    postfix = str(int(datetime.now().timestamp()*1e+6))
    parts = file_name.split('.')
    file_name_temporized = '.'.join(parts[:-1])
    file_name_temporized += f'_{postfix}_.{parts[-1]}'

    return file_name_temporized


def get_temporary_db_file():
    """ Returns the temporary DB file name full path. """

    # Get the directory
    temp_dir = get_temp_dir()
    # Temporise the default file name
    temp_file = file_name_temporize(DB_FILE)
    # Get the temporary file full path
    temp_file_path = temp_dir + temp_file
    # Return the temporary file full path
    return temp_file_path


def use_test_db(func):
    """ Switch test into using the test Database. """

    def wrapper(*args, **kwargs):

        # Save previous file
        db_file_prev = DB.db_file
        # Create random named temporary DB file
        tmp_db_file = get_temporary_db_file()
        # Switch connection to the temporary DB
        DB(tmp_db_file, recreate=True)

        # Try to implement the target function
        try:
            target_func_return = func(*args, **kwargs)

        # If we failed - remove the temporary DB anyway
        finally:
            # Switch connection to the previous DB file
            DB(db_file_prev)
            # Remove the temporary DB
            os.remove(tmp_db_file)

        # Return the result
        return target_func_return
    return wrapper
