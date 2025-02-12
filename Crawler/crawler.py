# from email.mime import application
import os
import glob
# from importlib import import_module
import importlib
import logging
import settings

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LOGLEVEL)

all_list = list()
json_list = list()

MODULE_PATH = "modules"


################################### FUNCTIONS
def get_applications():
    """
    Get all application by crawling all modules.
    """
    # iterate over all mpython files in directory crawler_configuration.module_path
    for f in glob.glob(os.path.dirname(__file__) + "/" + MODULE_PATH + "/*.py"):
        if os.path.isfile(f) and not os.path.basename(f).startswith('_'):
            all_list.append(os.path.basename(f)[:-3])

    __all__ = all_list

    # iterate over all modules
    for mymodule in __all__:
        if mymodule in settings.crawler_module_whitelist or len(settings.crawler_module_whitelist) == 0:
            LOGGER.info("Checking %s for downloads.", mymodule)
            # import module
            if __name__ == '__main__':
                # we call the crawler.py directly, so we import without the __package__
                mod = importlib.import_module(MODULE_PATH + "." + mymodule)
            else:
                # we call the crawler.py from elsewhere, so we import with the __package__
                mod = importlib.import_module(__package__ + "." + MODULE_PATH + "." + mymodule)
            # run modules function run()
            json_list.append(mod.run())
        else:
            LOGGER.info("Skipping crawler module %s, because of whitelist.", mymodule)
    return json_list


if __name__ == "__main__":
    print(getApplications())
