import os
import glob
from importlib import import_module
import importlib

all_list = list()
json_list = list()

### BASIC configuration
module_path = "modules"


def getApplications(relative_path=''):
    # iterate over all mpython files in directory crawler_configuration.module_path
    for f in glob.glob(os.path.dirname(__file__) + "/" + module_path + "/*.py"):
        if os.path.isfile(f) and not os.path.basename(f).startswith('_'):
            all_list.append(os.path.basename(f)[:-3])

    __all__ = all_list

    # iterate over all modules
    for mymodule in __all__:
        print("checking {module} for downloads.".format(module=mymodule))
        # import module
        if __name__ == '__main__':
            # we call the crawler.py directly, so we import without the __package__
            mod = importlib.import_module(module_path + "." + mymodule)
        else:
            # we call the crawler.py from elsewhere, so we import with the __package__
            mod = importlib.import_module(__package__ + "." + module_path + "." + mymodule)
        # run modules function run()
        json_list.append(mod.run())
    return json_list


if __name__ == "__main__":
    print(getApplications())
