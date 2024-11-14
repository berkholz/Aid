import logging
import os

LogLevel = logging.DEBUG

cwd_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_PATH = os.path.join(cwd_dir, 'downloads/')