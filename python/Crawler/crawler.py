# python
import os
import glob
import importlib
import logging
import settings
import psycopg2

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOGLEVEL)

all_list = list()
json_list = list()

MODULE_PATH = "modules"


################################### FUNCTIONS
def get_activated_modules():
    """
    Fetch activated modules from the PostgreSQL database.
    """
    activated_modules = []
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**settings.DB_CONNECTION)
        cursor = connection.cursor()
        # Query the config table for activated modules
        cursor.execute("SELECT app_name FROM config WHERE activated = TRUE;")
        activated_modules = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        LOGGER.error("Error fetching activated modules: %s", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return activated_modules

def get_applications():
    # TODO add function to only crawl specific modules
    # TODO add try/except
    """
    Get all application by crawling all modules.
    """
    activated_modules = get_activated_modules()

    # Iterate over all Python files in the modules directory
    for f in glob.glob(os.path.dirname(__file__) + "/" + MODULE_PATH + "/*.py"):
        if os.path.isfile(f) and not os.path.basename(f).startswith('_'):
            all_list.append(os.path.basename(f)[:-3])

    __all__ = all_list

    # iterate over all modules
    for mymodule in __all__:
        if mymodule in activated_modules:
            LOGGER.info("Checking %s for downloads.", mymodule)
            # Import module
            if __name__ == '__main__':
                mod = importlib.import_module(MODULE_PATH + "." + mymodule)
            else:
                mod = importlib.import_module(__package__ + "." + MODULE_PATH + "." + mymodule)
            # run modules function run()
            try:
                json_list.append(mod.run())
            except Exception as e:
                LOGGER.error("Error in module %s: %s", mymodule, e)
        else:
            LOGGER.info("Skipping crawler module %s, because it is not activated.", mymodule)
    return json_list

if __name__ == "__main__":
    print(get_applications())