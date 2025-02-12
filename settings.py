import logging
import os

# from main import LOGGER

LOGLEVEL = logging.INFO

cwd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_PATH = os.path.join(cwd_dir, 'downloads/')

crawler_module_whitelist = list()
# to define a whitelits for modules uncomment the line above and add your modules as list
# crawler_module_whitelist = ['adobe_enterprise']

CRAWLER_MODULE_REQUEST_TIMEOUT = 30
