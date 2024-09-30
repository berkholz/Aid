import os

import Db.database as db
import logging # import lib for LOGGING
import settings # import global settings

################################### VARIABLES
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=settings.LogLevel)

cwd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_PATH = os.path.join(cwd_dir, 'downloads/')


################################### FUNCTIONS

def get_newest_link(software, platform):
    """database request for download-link of newest version"""
    link = db.get_url_bin(software.lower(), platform.lower())
    return link
