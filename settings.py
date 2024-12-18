import logging
import os

# from main import LOGGER

LOGLEVEL = logging.INFO

cwd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_PATH = os.path.join(cwd_dir, 'downloads/')